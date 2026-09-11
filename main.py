import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Parkinson's Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

# Load model and scaler saved from your notebooks
try:
  model = joblib.load("models/parkinson_model.pkl")
  scaler = joblib.load("models/scaler.pkl")  # Load your preprocessing scaler
except Exception as e:
  print(f"Error loading model or scaler: {e}")


class ParkinsonsInput(BaseModel):
  fo: float
  fhi: float
  flo: float
  jitter_percent: float
  shimmer: float
  hnr: float


@app.post("/predict")
def predict(data: ParkinsonsInput):
  try:
    # 1. Convert input to raw array
    raw_features = np.array([[
        data.fo,
        data.fhi,
        data.flo,
        data.jitter_percent,
        data.shimmer,
        data.hnr,
    ]])

    # 2. Scale features using the exact scaler from your pre_processing notebook
    scaled_features = scaler.transform(raw_features)

    # 3. Predict using the model from your model_testing notebook
    prediction = model.predict(scaled_features)
    probability = model.predict_proba(scaled_features)[0][1] * 100

    return {
        "prediction": int(prediction[0]),
        "risk_probability": round(probability, 2),
        "status": (
            "High Risk of Parkinson's"
            if prediction[0] == 1
            else "Healthy Range"
        ),
    }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))