from fastapi import FastAPI,HTTPException,Query
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
def get_patient_data(patient_id: str):
    data=load_data()
    for patient in data:
        if patient["name"] == patient_id:
            return patient[patient_id]
        raise HTTPException(status_code=404, detail="Patient not found")

@app.get("./sort")
def sort_Data(sort_by:str=Query(...,description="Sort on basis of jitter"),order:str=Query('asc',description="Order of sorting is asc or desc")):
    valid_fields=["jitter","shimmer","NHR","HNR"]
    if sort_by not in valid_fields:
        raise HttpException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")
    if order not in ['asc','desc']:
        raise HttpException(status_code=400, detail="Invalid order. Valid orders are: 'asc' or 'desc'")
    data=load_data()
    sorted_data=sorted(data,key=lambda x:x[sort_by],reverse=(order=='desc'))