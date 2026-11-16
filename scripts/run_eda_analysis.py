from pathlib import Path

from src.analysis.correlation_analysis import export_correlation_heatmap, export_summary_statistics
from src.analysis.lag_analysis import (
    compute_lag_correlation_table,
    export_best_lag_table,
    export_lag_correlation_table,
    export_lag_heatmap,
)
from src.data.loader import load_sru_data
from src.data.preprocess import basic_preprocess


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    figures_dir = project_root / "outputs" / "figures"
    tables_dir = project_root / "outputs" / "tables"

    df = basic_preprocess(load_sru_data())
    feature_cols = ["a1", "a2", "a3", "a4", "a5"]
    target_cols = ["y1", "y2"]

    export_summary_statistics(df, tables_dir / "sru_summary_statistics.csv")
    export_correlation_heatmap(df, figures_dir / "sru_correlation_heatmap.png")

    lag_df = compute_lag_correlation_table(
        df=df,
        feature_cols=feature_cols,
        target_cols=target_cols,
        max_lag=12,
    )
    export_lag_correlation_table(lag_df, tables_dir / "sru_lag_correlation.csv")
    export_best_lag_table(lag_df, tables_dir / "sru_best_lag_summary.csv")

    for target in target_cols:
        export_lag_heatmap(
            lag_df=lag_df,
            target=target,
            output_path=figures_dir / f"sru_lag_heatmap_{target}.png",
        )

    print("EDA and lag analysis finished.")
    print(f"Figures saved to: {figures_dir}")
    print(f"Tables saved to: {tables_dir}")


if __name__ == "__main__":
    main()
