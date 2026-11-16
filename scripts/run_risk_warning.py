from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analysis.risk_warning import build_risk_table, save_risk_outputs
from src.visualization.risk_plots import export_error_curve, export_risk_curve


def main() -> None:
    project_root = PROJECT_ROOT
    tables_dir = project_root / "outputs" / "tables"
    figures_dir = project_root / "outputs" / "figures"
    itransformer_predictions = tables_dir / "itransformer_predictions.joblib"
    slstm_predictions = tables_dir / "slstm_predictions.joblib"
    prediction_file = itransformer_predictions if itransformer_predictions.exists() else slstm_predictions
    model_name = "itransformer" if prediction_file == itransformer_predictions else "slstm"

    alert_df = build_risk_table(
        prediction_file=prediction_file,
        split="test",
        calibration_split="val",
        warn_quantile=0.90,
        danger_quantile=0.95,
    )
    save_risk_outputs(alert_df, tables_dir, prefix=model_name)
    save_risk_outputs(alert_df, tables_dir, prefix="best_model")
    export_risk_curve(alert_df, figures_dir, model_name=model_name)
    export_error_curve(alert_df, figures_dir, model_name=model_name)
    export_risk_curve(alert_df, figures_dir, model_name="best_model")
    export_error_curve(alert_df, figures_dir, model_name="best_model")

    print("Risk warning analysis finished.")
    print(f"Model: {model_name}")
    print(f"Alert table saved to: {tables_dir / f'{model_name}_risk_alerts.csv'}")
    print(f"Risk summary saved to: {tables_dir / f'{model_name}_risk_summary.csv'}")
    print(f"Risk figures saved to: {figures_dir}")


if __name__ == "__main__":
    main()
