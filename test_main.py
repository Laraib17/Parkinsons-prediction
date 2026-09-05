from fastapi.testclient import TestClient
from apis import app
client=TestClient(app)
def test_read_root():
    res=client.get("/")
    assert res.status_code==200
    assert "message" in res.json() or res.json is not None

def test_prediction_ednpoint():
    payload={
        "feature1":0.5,
        "feature1":1.5
    }
    res=client.post("/predict",json=payload)