# 🎵 Spotify Customer Churn Prediction

Full-stack ML app — FastAPI backend + React frontend — trained on real Spotify user data.

## Dataset Features Used
| Column | Type | Description |
|---|---|---|
| subscription_type | categorical | Premium / Free |
| country | categorical | 10 countries (US, IN, UK, DE, ...) |
| avg_daily_minutes | float | Average daily listening time |
| number_of_playlists | int | Playlists created |
| top_genre | categorical | Favourite genre |
| skips_per_day | int | Daily skip count |
| support_tickets | int | Complaints raised |
| days_since_last_login | int | Recency |
| **churned** | int (target) | 0 = stayed, 1 = churned |

## Model Performance
- **Algorithm:** Gradient Boosting Classifier
- **Accuracy:** 80%
- **ROC-AUC:** 0.75
- **Churn Rate in Dataset:** 18.6%
- **Top Features:** avg_daily_minutes, engagement_score, days_since_last_login

---

## 🚀 Setup & Run

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Train the model (one-time)
python train_model.py

# Start the API
uvicorn app.main:app --reload --port 8000
```

API Docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

---

## 📡 API Endpoints

### POST /api/predict/
```json
{
  "subscription_type": "Premium",
  "country": "US",
  "avg_daily_minutes": 90,
  "number_of_playlists": 5,
  "top_genre": "Pop",
  "skips_per_day": 4,
  "support_tickets": 0,
  "days_since_last_login": 3
}
```

Response:
```json
{
  "churn_probability": 0.12,
  "churn_prediction": false,
  "risk_level": "Low",
  "top_risk_factors": ["Avg Daily Minutes", "Engagement Score", "Days Since Last Login"],
  "recommendation": "✅ User is healthy: continue standard engagement."
}
```

### GET /api/analytics/summary
Returns pre-computed analytics: churn rates by genre, country, subscription, feature importances.

---

## 🗂 Project Structure

```
spotify-churn/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── models/              # Trained model files (.pkl, .json)
│   │   ├── routes/
│   │   │   ├── predict.py
│   │   │   └── analytics.py
│   │   ├── services/
│   │   │   └── model_service.py
│   │   └── schemas/
│   │       └── user_schema.py
│   ├── data/
│   │   └── spotify_churn_dataset.csv
│   ├── train_model.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Home.jsx
    │   │   ├── Predict.jsx
    │   │   └── Analytics.jsx
    │   ├── services/
    │   │   └── api.js
    │   └── App.jsx
    ├── package.json
    └── vite.config.js
```
