from catboost import CatBoostRegressor
import pandas as pd


MODEL_PATH = "backend/explainability/model.cbm"
TEST_PATH = "backend/explainability/test.csv"


def load_model():
    model = CatBoostRegressor()
    model.load_model(MODEL_PATH)
    return model


def load_features(csv_path: str):
    df = pd.read_csv(csv_path)

    model = load_model()
    feature_names = model.feature_names_.copy()

    # на всякий случай убираем target/id/dt, если они там есть
    for col in ["target", "id", "dt"]:
        if col in feature_names:
            feature_names.remove(col)

    X = df[feature_names]

    # приводим категориальные признаки
    try:
        cat_idxs = model.get_cat_feature_indices()
        cat_cols = [feature_names[i] for i in cat_idxs]
    except Exception:
        cat_cols = []

    for col in cat_cols:
        if col in X.columns:
            X[col] = X[col].astype(str)

    return df, X, feature_names, cat_cols