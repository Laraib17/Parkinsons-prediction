from fastapi import FastAPI
import json
app=FastAPI()

def load_data():
    with open('./data/raw_data/pd.json','r') as f:
        data=json.load(f) 
    return data

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get('/about')
def about():
    return {"message": "This is a FastAPI application for Parkinson's prediction research."}

@app.get("/data")
def get_data():
    data=load_data() 
    return data

@app.get("/patients/{patient_id}")
def get_patient_data(patient_id: str=Path(...,description="Id of the patient in DB",example="phon_R01_S01_1")):
    data=load_data()
    for patient in data:
        if patient["name"] == patient_id:
            return patient["Jitter:DDP"]
    return({"error": "Patient not found"})