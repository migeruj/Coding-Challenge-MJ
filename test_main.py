from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_empployees_upsert():
    url = "http://localhost:8000/?upsert=true&table_name=employees"

    payload = {}
    files = [
        ('batch_file', (
        'hired_employees.csv', open('./hired_employees.csv', 'rb'),
        'text/csv'))
    ]
    headers = {
        'Content-Type': 'multipart/form-data',
        'Accept': 'application/json'
    }

    response = client.request("POST", url, headers=headers, data=payload, files=files)

    assert response.status_code == 200
    assert response.json() == {"message": "Accepted"}


