from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analysis.decision_support import build_decision_recommendations, save_decision_recommendations


def main() -> None:
    project_root = PROJECT_ROOT
    tables_dir = project_root / "outputs" / "tables"

    alert_path = tables_dir / "best_model_risk_alerts.csv"
    if not alert_path.exists():
        alert_path = tables_dir / "slstm_risk_alerts.csv"

    alert_df = pd.read_csv(alert_path)
    best_lag_df = pd.read_csv(tables_dir / "sru_best_lag_summary.csv")
    recommendations = build_decision_recommendations(alert_df, best_lag_df)
    output_path = tables_dir / "decision_recommendations.csv"
    save_decision_recommendations(recommendations, output_path)

    print("Decision support recommendations generated.")
    print(f"Saved to: {output_path}")
    print(recommendations.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
