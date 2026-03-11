from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserFeatures, PredictionResponse
from app.services.model_service import predict_churn

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
def predict(user: UserFeatures):
    try:
        return predict_churn(user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
