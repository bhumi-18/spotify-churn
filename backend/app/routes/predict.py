from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.schemas.user_schema import UserFeatures, PredictionResponse, PredictionRecord
from app.services.model_service import predict_churn
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
async def predict(user: UserFeatures):
    try:
        print("➡️ API HIT")
        # 1. Run ML prediction
        result = predict_churn(user.model_dump())
        print("✅ Prediction done")
        
        # 2. Build the complete record to store
        record = PredictionRecord(
            # Input data
            subscription_type     = user.subscription_type,
            country               = user.country,
            avg_daily_minutes     = user.avg_daily_minutes,
            number_of_playlists   = user.number_of_playlists,
            top_genre             = user.top_genre,
            skips_per_day         = user.skips_per_day,
            support_tickets       = user.support_tickets,
            days_since_last_login = user.days_since_last_login,
            # Prediction results
            churn_probability = result["churn_probability"],
            churn_prediction  = result["churn_prediction"],
            risk_level        = result["risk_level"],
            top_risk_factors  = result["top_risk_factors"],
            recommendation    = result["recommendation"],

            predicted_at = datetime.utcnow()
        )
        print("📦 Record created")

        # 3. Save to MongoDB (async, non-blocking)
        db = get_db()
        print("🧠 DB:", db)

        await db.predictions.insert_one(record.model_dump())
        print(f"💾 Saved prediction to MongoDB: risk={result['risk_level']}")

        # 4. Return result to frontend
        return result

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_prediction_history(limit: int = 50):
    """Get last N predictions from MongoDB"""
    try:
        db = get_db()
        cursor = db.predictions.find(
            {},
            {"_id": 0}   # exclude MongoDB _id field
        ).sort("predicted_at", -1).limit(limit)

        records = await cursor.to_list(length=limit)
        return {"total": len(records), "predictions": records}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_prediction_stats():
    """Live stats from all stored predictions"""
    try:
        db = get_db()
        total = await db.predictions.count_documents({})
        high  = await db.predictions.count_documents({"risk_level": "High"})
        med   = await db.predictions.count_documents({"risk_level": "Medium"})
        low   = await db.predictions.count_documents({"risk_level": "Low"})

        # Average churn probability
        pipeline = [{"$group": {"_id": None,
                                "avg_prob": {"$avg": "$churn_probability"}}}]
        avg_result = await db.predictions.aggregate(pipeline).to_list(1)
        avg_prob = round(avg_result[0]["avg_prob"] * 100, 1) if avg_result else 0

        return {
            "total_predictions": total,
            "high_risk":   high,
            "medium_risk": med,
            "low_risk":    low,
            "avg_churn_probability": avg_prob,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))