from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import joblib

app=FastAPI(title='Parkinsons prediction API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[''],
    allow_credentials=True,
    allow_methods=[''],
    allow_headers=[''],
)
try:
    model=joblib.load()