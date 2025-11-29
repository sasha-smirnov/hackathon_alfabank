from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import PredictRequest, PredictResponse, ExplainRequest, ExplainResponse, RecommendRequest, RecommendResponse
from services.recommendations import get_mock_recommendations


app = FastAPI(title="Income Prediction API (Mock Mode)")


# --- CORS: чтобы фронт мог делать запросы ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на хакатоне это ОК
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Здоровье сервиса ---
@app.get("/health")
def health():
    return {"status": "ok"}


# --- /predict (mock версия) ---
@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # Пока нет ML модели — возвращаем стабовые данные
    return PredictResponse(
        income=120000 + req.client_id * 10,
        confidence=0.85
    )


# --- /explain (mock версия) ---
@app.post("/explain", response_model=ExplainResponse)
def explain(req: ExplainRequest):
    mock_features = [
        {"name": "Возраст", "value": 30, "impact": 0.25},
        {"name": "Траты", "value": 40000, "impact": -0.15},
        {"name": "Скоринг", "value": 690, "impact": 0.10},
    ]
    return ExplainResponse(features=mock_features)


# --- /recommend ---
@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    products = get_mock_recommendations(req.client_id)
    return RecommendResponse(products=products)