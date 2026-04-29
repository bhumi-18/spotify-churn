from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ── Input schema (what user fills in the form) ────────────────
class UserFeatures(BaseModel):
    subscription_type:     str   = Field(..., description="Premium or Free")
    country:               str   = Field(..., description="Country code")
    avg_daily_minutes:     float = Field(..., ge=0)
    number_of_playlists:   int   = Field(..., ge=0)
    top_genre:             str
    skips_per_day:         int   = Field(..., ge=0)
    support_tickets:       int   = Field(..., ge=0)
    days_since_last_login: int   = Field(..., ge=0)

# ── Output schema (what API returns) ─────────────────────────
class PredictionResponse(BaseModel):
    churn_probability: float
    churn_prediction:  bool
    risk_level:        str
    top_risk_factors:  List[str]
    recommendation:    str

# ── MongoDB stored document schema ───────────────────────────
class PredictionRecord(BaseModel):
    """Complete record stored in MongoDB"""
    # User input fields
    subscription_type:     str
    country:               str
    avg_daily_minutes:     float
    number_of_playlists:   int
    top_genre:             str
    skips_per_day:         int
    support_tickets:       int
    days_since_last_login: int
    # Prediction results
    churn_probability:     float
    churn_prediction:      bool
    risk_level:            str
    top_risk_factors:      List[str]
    recommendation:        str
    # Metadata
    predicted_at:          datetime = Field(default_factory=datetime.utcnow)
    model_version:         str = "1.0"

# ── Schema for manual user data entry (for future training) ──
class UserDataEntry(BaseModel):
    """User submits their actual churn status for retraining"""
    subscription_type:     str
    country:               str
    avg_daily_minutes:     float
    number_of_playlists:   int
    top_genre:             str
    skips_per_day:         int
    support_tickets:       int
    days_since_last_login: int
    churned:               int = Field(..., ge=0, le=1,
                               description="Actual churn: 0=stayed, 1=churned")