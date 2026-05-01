import pytest
from django.contrib.auth import get_user

@pytest.mark.django_db
def test_user_registrations_api(client):
    payload = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "password",
        "first_name": "name",
        "last_name": "lastName"
    }
    responce = client.post("/api/accounts/register", payload, format='json')
    assert responce.status_code == 200
    
@pytest.mark.django_db
def test_admin_login(client, user_credentials_admin, default_test_users_list):
    login_payload = {
        "username": user_credentials_admin["username"],
        "password": user_credentials_admin["password"]
    }
    responce = client.post("/api/accounts/login", login_payload, format='json')
    assert responce.status_code == 200
    user = get_user(client)
    
    assert user.is_authenticated
    assert user.username == user_credentials_admin["username"]
    assert user.email == user_credentials_admin["email"]
    
@pytest.mark.django_db
def test_player_login(client, user_credentials_player, default_test_users_list):
    login_payload = {
        "username": user_credentials_player["username"],
        "password": user_credentials_player["password"]
    }
    responce = client.post("/api/accounts/login", login_payload, format='json')
    assert responce.status_code == 200
    user = get_user(client)
    
    assert user.is_authenticated
    assert user.username == user_credentials_player["username"]
    assert user.email == user_credentials_player["email"]
    
@pytest.mark.django_db
def test_player_logout_api(auth_client_player):
    responce = auth_client_player.post("/api/accounts/logout")
    assert responce.status_code == 200