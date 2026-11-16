import pandas as pd

from src.app.services.platform_enhancement import (
    build_alert_history,
    build_alert_event_summary,
    build_feature_contribution_summary,
    build_joint_risk_analysis,
    build_rule_diagnostics,
    build_risk_work_orders,
    build_threshold_preview,
    enrich_risk_alerts,
    evaluate_rule_condition,
    match_knowledge,
)


def test_platform_enhancement_services():
    risk_alert_df = pd.DataFrame(
        [
            {
                "time_step": 1,
                "target": "y1",
                "true_value": 0.11,
                "pred_value": 0.12,
                "abs_error": 0.01,
                "error_warn_threshold": 0.02,
                "error_danger_threshold": 0.03,
                "value_warn_threshold": 0.10,
                "value_danger_threshold": 0.13,
                "risk_level": "warning",
                "is_alert": True,
            },
            {
                "time_step": 2,
                "target": "y1",
                "true_value": 0.12,
                "pred_value": 0.14,
                "abs_error": 0.04,
                "error_warn_threshold": 0.02,
                "error_danger_threshold": 0.03,
                "value_warn_threshold": 0.10,
                "value_danger_threshold": 0.13,
                "risk_level": "danger",
                "is_alert": True,
            },
            {
                "time_step": 1,
                "target": "y2",
                "true_value": 0.18,
                "pred_value": 0.19,
                "abs_error": 0.01,
                "error_warn_threshold": 0.02,
                "error_danger_threshold": 0.03,
                "value_warn_threshold": 0.18,
                "value_danger_threshold": 0.22,
                "risk_level": "warning",
                "is_alert": True,
            },
        ]
    )
    decision_df = pd.DataFrame(
        [
            {
                "target": "y1",
                "risk_level": "danger",
                "time_step": 2,
                "related_feature": "a3",
                "lag": 12,
                "recommendation": "检查空气配比",
                "priority": "高",
            }
        ]
    )
    expert_df = pd.DataFrame(
        [
            {"knowledge_id": "KB1", "target": "y1", "risk_level": "danger"},
            {"knowledge_id": "KB2", "target": "通用", "risk_level": "danger"},
            {"knowledge_id": "KB3", "target": "y2", "risk_level": "warning"},
        ]
    )

    preview_df = build_threshold_preview(
        risk_alert_df,
        target="y1",
        warn_value=0.10,
        danger_value=0.13,
        warn_error=0.02,
        danger_error=0.03,
    )
    assert not preview_df.empty
    assert set(preview_df["custom_risk_level"]) == {"warning", "danger"}

    history_df = build_alert_history(risk_alert_df, decision_df)
    assert not history_df.empty
    assert "event_tag" in history_df.columns
    assert "recommendation" in history_df.columns

    matched_df = match_knowledge(expert_df, target="y1", risk_level="danger")
    assert len(matched_df) == 2

    enriched_df = enrich_risk_alerts(risk_alert_df)
    assert "risk_score" in enriched_df.columns
    assert "trigger_reason" in enriched_df.columns
    assert "continuous_alert_count" in enriched_df.columns
    assert enriched_df[enriched_df["target"] == "y1"]["continuous_alert_count"].max() == 2

    joint_df = build_joint_risk_analysis(enriched_df)
    assert not joint_df.empty
    assert "joint_pattern" in joint_df.columns

    contribution_df = build_feature_contribution_summary(decision_df, target="y1")
    assert not contribution_df.empty
    assert contribution_df.iloc[0]["related_feature"] == "a3"

    persisted_history_df = pd.DataFrame(
        [
            {
                "event_id": "y1-event-1",
                "target": "y1",
                "risk_level": "danger",
                "time_step": 2,
                "status": "处理中",
                "handler": "operator-a",
                "comment": "air loop checked",
                "review_result": "真实风险",
            }
        ]
    )
    work_order_df = build_risk_work_orders(risk_alert_df, decision_df, expert_df, persisted_history_df)
    assert not work_order_df.empty
    assert "work_order_id" in work_order_df.columns
    assert "recommended_action" in work_order_df.columns
    y1_order = work_order_df[work_order_df["target"] == "y1"].iloc[0]
    assert y1_order["status"] == "处理中"
    assert y1_order["owner"] == "operator-a"
    assert y1_order["related_feature"] == "a3"
    assert y1_order["priority"] in {"P1", "P2"}


def test_rule_diagnostics_and_alert_event_summary():
    risk_alert_df = pd.DataFrame(
        [
            {
                "time_step": 1,
                "target": "y1",
                "true_value": 0.11,
                "pred_value": 0.14,
                "abs_error": 0.04,
                "error_warn_threshold": 0.02,
                "error_danger_threshold": 0.03,
                "value_warn_threshold": 0.10,
                "value_danger_threshold": 0.13,
                "risk_level": "danger",
                "is_alert": True,
            },
            {
                "time_step": 2,
                "target": "y1",
                "true_value": 0.12,
                "pred_value": 0.145,
                "abs_error": 0.035,
                "error_warn_threshold": 0.02,
                "error_danger_threshold": 0.03,
                "value_warn_threshold": 0.10,
                "value_danger_threshold": 0.13,
                "risk_level": "danger",
                "is_alert": True,
            },
            {
                "time_step": 3,
                "target": "y1",
                "true_value": 0.13,
                "pred_value": 0.15,
                "abs_error": 0.032,
                "error_warn_threshold": 0.02,
                "error_danger_threshold": 0.03,
                "value_warn_threshold": 0.10,
                "value_danger_threshold": 0.13,
                "risk_level": "danger",
                "is_alert": True,
            },
        ]
    )
    expert_df = pd.DataFrame(
        [
            {
                "knowledge_id": "KB1",
                "target": "y1",
                "risk_level": "danger",
                "focus_area": "H2S danger",
                "trigger_pattern": "y1 danger",
                "condition_expression": "target == y1 AND risk_level == danger AND risk_score >= 80",
                "check_item": "check a3",
                "recommendation": "adjust air",
                "related_dataset_variable": "y1/a3",
                "confidence": "高",
            },
            {
                "knowledge_id": "KB2",
                "target": "通用",
                "risk_level": "danger",
                "focus_area": "common danger",
                "trigger_pattern": "danger",
                "condition_expression": "target == y2",
                "check_item": "check analyzer",
                "recommendation": "verify sensor",
                "related_dataset_variable": "y1/y2",
                "confidence": "高",
            },
        ]
    )

    enriched_df = enrich_risk_alerts(risk_alert_df)
    diagnostics_df = build_rule_diagnostics(expert_df, enriched_df, target="y1", risk_level="danger")
    assert not diagnostics_df.empty
    assert diagnostics_df.iloc[0]["match_score"] >= 80
    assert "match_reason" in diagnostics_df.columns
    assert "condition_expression" in diagnostics_df.columns
    assert diagnostics_df.iloc[0]["condition_expression"] == "target == y1 AND risk_level == danger AND risk_score >= 80"
    assert diagnostics_df.iloc[0]["match_reason"].startswith("condition matched")
    assert diagnostics_df[diagnostics_df["knowledge_id"] == "KB2"].iloc[0]["match_score"] < diagnostics_df.iloc[0]["match_score"]

    event_summary_df = build_alert_event_summary(enriched_df)
    assert not event_summary_df.empty
    assert event_summary_df.iloc[0]["duration"] == 3
    assert "upgrade_advice" in event_summary_df.columns


def test_rule_condition_expression_evaluator():
    alert = pd.Series(
        {
            "target": "y1",
            "risk_level": "danger",
            "risk_score": 92,
            "continuous_alert_count": 4,
            "trigger_reason": "value danger",
        }
    )

    matched, reason = evaluate_rule_condition(
        "target == y1 AND risk_level == danger AND risk_score >= 90 AND continuous_alert_count >= 3",
        alert,
    )
    assert matched
    assert "risk_score >= 90.0 (ok)" in reason

    matched, reason = evaluate_rule_condition("target == y2 OR risk_score < 50", alert)
    assert not matched
    assert "target == y2" in reason
