import pytest
from unittest.mock import patch


# 1. test_get_profile_no_auth
def test_get_profile_no_auth(client):
    response = client.get('/api/profile')
    assert response.status_code == 401
    assert "error" in response.get_json()


# 2. test_get_profile_bad_token_format
def test_get_profile_bad_token_format(client):
    response = client.get('/api/profile', headers={'Authorization': 'InvalidFormat'})
    assert response.status_code == 401
    assert "error" in response.get_json()


# 3. test_get_profile_invalid_token
@patch('firebase_admin.auth.verify_id_token')
def test_get_profile_invalid_token(mock_verify, client):
    mock_verify.side_effect = Exception("Invalid token")
    response = client.get('/api/profile', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    assert "error" in response.get_json()


# 4. test_get_profile_success
def test_get_profile_success(client, mock_firebase_auth, mock_firestore):
    response = client.get('/api/profile', headers={'Authorization': 'Bearer valid_token'})
    assert response.status_code == 200
    data = response.get_json()
    assert "uid" in data
    assert "profile" in data
    assert data["profile"]["first_name"] == "Test"


# 5. test_create_profile_missing_fields
def test_create_profile_missing_fields(client, mock_firebase_auth):
    payload = {"first_name": "Jane", "last_name": "Doe"}  # missing student_id
    response = client.post('/api/profile', headers={'Authorization': 'Bearer valid_token'}, json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()


# 6. test_create_profile_success (bonus)
def test_create_profile_success(client, mock_firebase_auth, mock_firestore):
    payload = {"first_name": "Jane", "last_name": "Doe", "student_id": "A1234567"}
    response = client.post('/api/profile', headers={'Authorization': 'Bearer valid_token'}, json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "profile" in data


# 7. test_update_profile_invalid_field (bonus)
def test_update_profile_invalid_field(client, mock_firebase_auth):
    payload = {"first_name": "Jane", "last_name": "Doe", "student_id": "A1234567", "age": 25}
    response = client.put('/api/profile', headers={'Authorization': 'Bearer valid_token'}, json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data
    assert "age" in str(data)