import joblib
import numpy as np
import pandas as pd
import os

BASE = os.path.join(os.path.dirname(__file__), '..', 'models')

model           = joblib.load(os.path.join(BASE, 'churn_model.pkl'))
scaler          = joblib.load(os.path.join(BASE, 'scaler.pkl'))
genre_encoder   = joblib.load(os.path.join(BASE, 'genre_encoder.pkl'))
country_encoder = joblib.load(os.path.join(BASE, 'country_encoder.pkl'))
FEATURES        = joblib.load(os.path.join(BASE, 'features.pkl'))

RECOMMENDATIONS = {
    "High": "🚨 Immediate action needed: offer a discount, send a re-engagement email, or provide a free Premium trial.",
    "Medium": "⚠️ Monitor closely: send personalised playlist recommendations and in-app nudges.",
    "Low": "✅ User is healthy: continue standard engagement and periodic check-ins.",
}

def predict_churn(data: dict) -> dict:
    # Encode categoricals
    is_premium      = 1 if data['subscription_type'] == 'Premium' else 0
    genre_encoded   = int(genre_encoder.transform([data['top_genre']])[0])
    country_encoded = int(country_encoder.transform([data['country']])[0])

    # Feature engineering (must match training)
    avg_daily_minutes     = max(0, data['avg_daily_minutes'])
    engagement_score      = avg_daily_minutes / (data['skips_per_day'] + 1)
    risk_score            = data['days_since_last_login'] * data['support_tickets'] + data['skips_per_day']

    row = {
        'avg_daily_minutes':     avg_daily_minutes,
        'number_of_playlists':   data['number_of_playlists'],
        'skips_per_day':         data['skips_per_day'],
        'support_tickets':       data['support_tickets'],
        'days_since_last_login': data['days_since_last_login'],
        'is_premium':            is_premium,
        'genre_encoded':         genre_encoded,
        'country_encoded':       country_encoded,
        'engagement_score':      engagement_score,
        'risk_score':            risk_score,
    }

    df = pd.DataFrame([row])[FEATURES]
    df_scaled = scaler.transform(df)

    prob       = float(model.predict_proba(df_scaled)[0][1])
    prediction = prob >= 0.5

    risk = "High" if prob >= 0.6 else ("Medium" if prob >= 0.3 else "Low")

    # Top risk factors
    importances  = model.feature_importances_
    sorted_feats = sorted(zip(FEATURES, importances), key=lambda x: -x[1])
    top_factors  = [f.replace('_', ' ').title() for f, _ in sorted_feats[:3]]

    return {
        "churn_probability": round(prob, 4),
        "churn_prediction":  prediction,
        "risk_level":        risk,
        "top_risk_factors":  top_factors,
        "recommendation":    RECOMMENDATIONS[risk],
    }
