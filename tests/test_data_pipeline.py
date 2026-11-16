from src.data.loader import load_sru_data
from src.data.preprocess import basic_preprocess


def test_data_pipeline():
    df = load_sru_data()
    cleaned = basic_preprocess(df)
    assert not cleaned.empty
