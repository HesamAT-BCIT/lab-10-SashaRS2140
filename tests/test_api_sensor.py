import pytest


# 1. test_sensor_data_no_api_key
def test_sensor_data_no_api_key(client):
    response = client.post('/api/sensor_data', json={"temperature": 25})
    assert response.status_code == 401
    assert "error" in response.get_json()


# 2. test_sensor_data_wrong_key
def test_sensor_data_wrong_key(client):
    response = client.post('/api/sensor_data', headers={'X-API-Key': 'wrong_key'}, json={"temperature": 25})
    assert response.status_code == 401
    assert "error" in response.get_json()


# 3. test_sensor_data_valid_key
def test_sensor_data_valid_key(client, mock_firestore):
    response = client.post('/api/sensor_data', headers={'X-API-Key': 'test-sensor-key'}, json={"temperature": 25})
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert "id" in data