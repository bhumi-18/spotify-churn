from pydantic import BaseModel, Field
from typing import List

COUNTRIES  = ["US", "PK", "DE", "IN", "UK", "BR", "FR", "CA", "RU", "AU"]
GENRES     = ["Electronic", "Pop", "Classical", "Jazz", "Country", "Rock", "Hip-Hop"]
SUB_TYPES  = ["Premium", "Free"]

class UserFeatures(BaseModel):
    subscription_type:     str   = Field(..., description="Premium or Free")
    country:               str   = Field(..., description="2-letter country code")
    avg_daily_minutes:     float = Field(..., ge=0,  description="Average daily listening minutes")
    number_of_playlists:   int   = Field(..., ge=0,  description="Number of playlists created")
    top_genre:             str   = Field(..., description="Favourite genre")
    skips_per_day:         int   = Field(..., ge=0,  description="Average skips per day")
    support_tickets:       int   = Field(..., ge=0,  description="Number of support tickets raised")
    days_since_last_login: int   = Field(..., ge=0,  description="Days since last login")

class PredictionResponse(BaseModel):
    churn_probability:  float
    churn_prediction:   bool
    risk_level:         str
    top_risk_factors:   List[str]
    recommendation:     str
