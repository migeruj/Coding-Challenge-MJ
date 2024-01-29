from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_empployees_insert():
    url = "http://localhost:8000/?upsert=false&table_name=employees"

    payload = {}
    files = [
        ('batch_file', (
        'hired_employees.csv', open('./hired_employees.csv', 'rb'),
        'text/csv'))
    ]

    response = client.request("POST", url, data=payload, files=files)

    assert response.status_code == 200 or response.status_code == 410


def test_jobs_insert():
    url = "http://localhost:8000/?upsert=false&table_name=jobs"

    payload = {}
    files = [
        ('batch_file', (
        'jobs.csv', open('./jobs.csv', 'rb'),
        'text/csv'))
    ]

    response = client.request("POST", url, data=payload, files=files)

    assert response.status_code == 200 or response.status_code == 410


def test_departments_insert():
    url = "http://localhost:8000/?upsert=false&table_name=departments"

    payload = {}
    files = [
        ('batch_file', (
        'departments.csv', open('./departments.csv', 'rb'),
        'text/csv'))
    ]

    response = client.request("POST", url, data=payload, files=files)

    assert response.status_code == 200 or response.status_code == 410


def test_empployees_upsert():
    url = "http://localhost:8000/?upsert=true&table_name=employees"

    payload = {}
    files = [
        ('batch_file', (
        'hired_employees.csv', open('./hired_employees.csv', 'rb'),
        'text/csv'))
    ]

    response = client.request("POST", url, data=payload, files=files)

    assert response.status_code == 200
    assert response.json() == {"message": "Accepted"}

def test_jobs_upsert():
    url = "http://localhost:8000/?upsert=true&table_name=jobs"

    payload = {}
    files = [
        ('batch_file', (
        'jobs.csv', open('./jobs.csv', 'rb'),
        'text/csv'))
    ]

    response = client.request("POST", url, data=payload, files=files)

    assert response.status_code == 200
    assert response.json() == {"message": "Accepted"}

def test_departments_upsert():
    url = "http://localhost:8000/?upsert=true&table_name=departments"

    payload = {}
    files = [
        ('batch_file', (
        'departments.csv', open('./departments.csv', 'rb'),
        'text/csv'))
    ]

    response = client.request("POST", url, data=payload, files=files)

    assert response.status_code == 200
    assert response.json() == {"message": "Accepted"}
def test_wrong_for_employees():
    url = "http://localhost:8000/?upsert=true&table_name=employees"

    payload = {}
    files = [
        ('batch_file', (
        'departments.csv', open('./departments.csv', 'rb'),
        'text/csv'))
    ]

    response = client.request("POST", url, data=payload, files=files)

    assert response.status_code == 412
    assert response.json() == {"detail": "Check your batch file, Doesn't belong to employees schema"}

def test_wrong_for_departments():
    url = "http://localhost:8000/?upsert=true&table_name=departments"

    payload = {}
    files = [
        ('batch_file', (
        'hired_employees.csv', open('./hired_employees.csv', 'rb'),
        'text/csv'))
    ]

    response = client.request("POST", url, data=payload, files=files)

    assert response.status_code == 412
    assert response.json() == {"detail": "Check your batch file, Doesn't belong to departments schema"}


def test_wrong_for_jobs():
    url = "http://localhost:8000/?upsert=true&table_name=jobs"

    payload = {}
    files = [
        ('batch_file', (
        'hired_employees.csv', open('./hired_employees.csv', 'rb'),
        'text/csv'))
    ]

    response = client.request("POST", url, data=payload, files=files)

    assert response.status_code == 412
    assert response.json() == {"detail": "Check your batch file, Doesn't belong to jobs schema"}


