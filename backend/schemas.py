from pydantic import BaseModel
from typing import List, Optional

class PredictRequest(BaseModel):
    client_id: int

class PredictResponse(BaseModel):
    income: float
    confidence: Optional[float] = None

class ExplainRequest(BaseModel):
    client_id: int

class FeatureImpact(BaseModel):
    name: str
    value: Optional[float | int | str]
    impact: float

class ExplainResponse(BaseModel):
    features: List[FeatureImpact]

class RecommendRequest(BaseModel):
    client_id: int

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    reason: Optional[str] = None

class RecommendResponse(BaseModel):
    products: List[Product]