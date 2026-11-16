from pathlib import Path

from src.visualization.result_plots import export_model_comparison_table, export_prediction_curve


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    tables_dir = project_root / "outputs" / "tables"
    figures_dir = project_root / "outputs" / "figures"

    export_model_comparison_table(
        metrics_files={
            "xgboost_static": tables_dir / "baseline_metrics.csv",
            "xgboost_lag": tables_dir / "lag_baseline_metrics.csv",
            "slstm": tables_dir / "slstm_metrics.csv",
            "va_lstm": tables_dir / "va_lstm_metrics.csv",
            "itransformer": tables_dir / "itransformer_metrics.csv",
        },
        output_path=tables_dir / "model_comparison_metrics.csv",
    )

    export_prediction_curve(
        prediction_file=tables_dir / "lag_baseline_predictions.joblib",
        output_dir=figures_dir,
        model_name="xgboost_lag",
        split="test",
    )
    export_prediction_curve(
        prediction_file=tables_dir / "slstm_predictions.joblib",
        output_dir=figures_dir,
        model_name="slstm",
        split="test",
    )
    export_prediction_curve(
        prediction_file=tables_dir / "va_lstm_predictions.joblib",
        output_dir=figures_dir,
        model_name="va_lstm",
        split="test",
    )
    export_prediction_curve(
        prediction_file=tables_dir / "itransformer_predictions.joblib",
        output_dir=figures_dir,
        model_name="itransformer",
        split="test",
    )

    print("Result visualization finished.")
    print(f"Comparison table saved to: {tables_dir / 'model_comparison_metrics.csv'}")
    print(f"Prediction curves saved to: {figures_dir}")


if __name__ == "__main__":
    main()
