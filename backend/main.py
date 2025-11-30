from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import PredictRequest, PredictResponse, ExplainRequest, ExplainResponse, RecommendRequest, RecommendResponse
from explainability.recommendations import build_recommendations
from explainability.explainability import load_model, load_data, get_shap_explainer, explain_single_prediction, feature_category, feature_names

model = load_model("model.cbm")
data = load_data("data.csv")
explainer = get_shap_explainer(model)

app = FastAPI(title="Income Prediction API (Mock)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    row = data[data["id"] == req.client_id].iloc[0]

    income = model.predict(row.to_frame().T)[0]

    return {
        "income": float(income),
        "confidence": 0.85
    }

@app.post("/explain", response_model=ExplainResponse)
def explain(req: ExplainRequest):
    row = data[data["id"] == req.client_id].iloc[0]

    result = explain_single_prediction(
        explainer=explainer,
        model=model,
        x_row=row,
        feature_names=feature_names,
        feature_category=feature_category
    )

    return {
        "prediction": result["prediction"],
        "base_value": result["base_value"],
        "features": result["contributions"]
    }


@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    row = data[data["id"] == req.client_id].iloc[0]

    predicted_income = float(model.predict(row.to_frame().T)[0])

    shap_result = explain_single_prediction(
        explainer=explainer,
        model=model,
        x_row=row,
        feature_names=feature_names,
        feature_category=feature_category,
        top_k=40
    )

    recommendations = build_recommendations(
        predicted_income=predicted_income,
        features_row=row.to_dict(),
        shap_explanation=shap_result
    )

    return RecommendResponse(products=recommendations["products"])
