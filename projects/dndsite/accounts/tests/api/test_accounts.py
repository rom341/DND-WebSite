import pytest
from django.contrib.auth import get_user


@pytest.mark.django_db
def test_user_registrations(client):
    payload = dict(
        first_name = "name",
        last_name = "lastName",
        email = "testuser@gmail.com",
        username="testuser",
        password1="password",
        password2="password"
    )
    responce = client.post("/accounts/register/", payload)
    assert responce.status_code == 302
    
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
def test_admin_logout(auth_client_admin):
    responce = auth_client_admin.post("/accounts/logout/")
    assert responce.status_code == 302
    
@pytest.mark.django_db
def test_player_logout(auth_client_player):
    responce = auth_client_player.post("/accounts/logout/")
    assert responce.status_code == 302