from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import predict, analytics, users
from app.database import connect_db, close_db

app = FastAPI(title="Spotify Churn Prediction API", version="2.0.0")

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://*.vercel.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Database lifecycle ────────────────────────────────────────
@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

# ── Routes ────────────────────────────────────────────────────
app.include_router(predict.router,   prefix="/api/predict",   tags=["Prediction"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(users.router,     prefix="/api/users",     tags=["Users"])

@app.get("/")
def root():
    return {"message": "🎵 Spotify Churn API v2.0 with MongoDB"}