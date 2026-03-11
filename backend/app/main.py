from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import predict, analytics

app = FastAPI(title="Spotify Churn Prediction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://*.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router,   prefix="/api/predict",   tags=["Prediction"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])

@app.get("/")
def root():
    return {"message": "🎵 Spotify Churn Prediction API is running!"}
