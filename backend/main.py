from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import PredictRequest, PredictResponse, ExplainRequest, ExplainResponse, RecommendRequest, RecommendResponse
from services.recommendations import get_mock_recommendations
from explainability.recommendations import build_recommendations


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

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    return PredictResponse(
        income=120000 + req.client_id * 10,
        confidence=0.85
    )

@app.post("/explain", response_model=ExplainResponse)
def explain(req: ExplainRequest):
    mock_features = [
        {"name": "Возраст", "value": 30, "impact": 0.25},
        {"name": "Траты", "value": 40000, "impact": -0.15},
        {"name": "Скоринг", "value": 690, "impact": 0.10},
    ]
    return ExplainResponse(features=mock_features)

@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    pred_income = 100_000
    shap_explanation = None
    features_row = {
        "blacklist_flag": 0,
        "total_sum": 0,
        "hdb_bki_total_active_products": 2
    }
    rec = build_recommendations(
        predicted_income=pred_income,
        features_row=features_row,
        shap_explanation=shap_explanation,
    )
    return RecommendResponse(products=rec["products"])