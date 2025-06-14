import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_activities(client):
    response = client.get('/get_activities')
    assert response.status_code == 200  


def test_create_student_success(client):
    response = client.post('/create_student', json={
        "student_id": "student3",
        "password": "teste3"
    })

    assert response.status_code == 201


def test_create_student_fail(client):
    response = client.post('/create_student', json={
        "student_id": "student1",
        "password": "teste"
    })

    assert response.status_code == 500


def test_enroll_activity_success(client):
    response = client.post('/enroll_activity', json={
        "student_id": "student1",
        "password": "teste",
        "activity_ids": [0, 1]
    })

    assert response.status_code == 200
    assert response.get_json() == [1]


def test_enroll_activity_auth_fail(client):
    response = client.post('/enroll_activity', json={
        "student_id": "student2",
        "password": "teste",
        "activity_ids": [1, 2]
    })

    assert response.status_code == 401
    assert b"Wrong password or ID" in response.data
