from fastapi.testclient import TestClient
from apis import app
client=TestClient(app)
def test_read_root():
    res=client.get("/")
    assert res.status_code==200
    assert "message" in res.json() or res.json is not None

def test_get_patient_data():
    patient_id = "phon_R01_S01_1"
    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("name") == patient_id
    assert "MDVP:Fo(Hz)" in data