from pathlib import Path

import pandas as pd

from src.alerts.alert_logger import append_alert_event, query_alert_history, update_alert_status
from src.config.threshold_config import (
    build_threshold_config_from_alerts,
    get_thresholds_for_target,
    load_threshold_history,
    save_threshold_config,
    update_threshold_for_target,
)
from src.data.loader import load_sru_data
from src.data.preprocess import basic_preprocess
from src.app.services.model_explanation import build_sequence_explanation
from src.inference.inference_service import SRUInferenceService
from src.inference.predictor import SRUPredictor, resolve_prediction_file
from src.knowledge.expert_rules import load_expert_rules, query_expert_rules


def test_threshold_config_roundtrip(tmp_path):
    alert_df = pd.DataFrame(
        [
            {
                "target": "y1",
                "value_warn_threshold": 0.1,
                "value_danger_threshold": 0.2,
                "error_warn_threshold": 0.01,
                "error_danger_threshold": 0.02,
                "threshold_source": "val",
            }
        ]
    )
    config = build_threshold_config_from_alerts(alert_df)
    config_path = tmp_path / "thresholds.json"
    save_threshold_config(config, config_path)

    loaded = get_thresholds_for_target("y1", config_path)
    assert loaded["value_warn_threshold"] == 0.1
    assert loaded["source"] == "val"

    history_path = tmp_path / "threshold_versions.jsonl"
    update_threshold_for_target(
        "y1",
        {
            "value_warn_threshold": 0.12,
            "value_danger_threshold": 0.22,
            "error_warn_threshold": 0.02,
            "error_danger_threshold": 0.03,
        },
        path=config_path,
        history_path=history_path,
        operator="tester",
        reason="unit test",
    )
    updated = get_thresholds_for_target("y1", config_path)
    assert updated["version"] == 1
    assert updated["updated_by"] == "tester"
    history_df = load_threshold_history(history_path)
    assert len(history_df) == 1


def test_predictor_can_read_prediction_bundle():
    prediction_file = resolve_prediction_file()
    predictor = SRUPredictor(prediction_file)
    description = predictor.describe()
    sample = predictor.predict_at_time_step(target=description["target_cols"][0], time_step=0)

    assert Path(description["prediction_file"]).exists()
    assert sample["target"] in description["target_cols"]
    assert "pred_value" in sample


def test_inference_service_integrates_prediction_threshold_and_knowledge():
    expert_df = load_expert_rules()
    service = SRUInferenceService()
    result = service.predict_with_knowledge(target="y1", time_step=1082, expert_df=expert_df)

    assert result["risk_level"] == "danger"
    assert result["threshold"]["value_level"] == "danger"
    assert "reliability" in result
    assert result["reliability"]["reliability_label"] in {"高可靠", "中等可靠", "需人工复核", "稳定"}
    assert len(result["expert_rules"]) >= 1
    assert result["recommendation"]


def test_online_sequence_model_inference_connects_to_knowledge():
    df = basic_preprocess(load_sru_data())
    service = SRUInferenceService()
    result = service.predict_sequence_with_knowledge(
        input_sequence=df[["a1", "a2", "a3", "a4", "a5"]].tail(12),
        target="y1",
        expert_df=load_expert_rules(),
    )

    assert result["prediction"]["source"] == "online_sequence_model"
    assert "pred_value" in result["prediction"]
    assert result["reliability"]["reliability_label"] in {"高可靠", "中等可靠", "需人工复核", "稳定"}
    assert "reliability_reason" in result["reliability"]
    assert "recommendation" in result


def test_sequence_explanation_service_returns_ranked_features():
    df = basic_preprocess(load_sru_data())
    predictor = SRUPredictor()
    result = build_sequence_explanation(predictor, df, target="y1")

    assert result["target"] == "y1"
    assert result["baseline_pred"] is not None
    assert len(result["top_features"]) >= 1
    assert "contribution_table" in result


def test_expert_rules_and_alert_logger(tmp_path):
    expert_df = load_expert_rules()
    matched = query_expert_rules(expert_df, target="y1", risk_level="danger")
    assert not matched.empty

    history_path = tmp_path / "alert_history.csv"
    append_alert_event(
        {
            "time_step": 12,
            "target": "y1",
            "risk_level": "danger",
            "pred_value": 0.12,
            "true_value": 0.11,
            "abs_error": 0.01,
            "related_feature": "a3",
            "lag": 12,
            "recommendation": "检查空气配比",
            "priority": "高",
            "status": "未处理",
            "handler": "tester",
            "comment": "unit test",
        },
        history_path,
    )
    queried = query_alert_history(history_path, target="y1", risk_level="danger", keyword="air")
    assert queried.empty

    queried = query_alert_history(history_path, target="y1", risk_level="danger", keyword="unit")
    assert len(queried) == 1

    event_id = queried.iloc[0]["event_id"]
    update_alert_status(
        event_id,
        "已恢复",
        path=history_path,
        handler="tester",
        comment="resolved",
        review_result="真实风险",
    )
    resolved = query_alert_history(history_path, target="y1", risk_level="danger", status="已恢复")
    assert len(resolved) == 1
    assert resolved.iloc[0]["review_result"] == "真实风险"
