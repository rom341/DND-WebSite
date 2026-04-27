import pytest

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
def test_admin_login(client, user_credentials_player):
    responce = client.post("/accounts/register/", user_credentials_player)
    assert responce.status_code == 302
    
@pytest.mark.django_db
def test_player_login(client, user_credentials_player):
    responce = client.post("/accounts/register/", user_credentials_player)
    assert responce.status_code == 302
    
@pytest.mark.django_db
def test_admin_logout(auth_client_admin):
    responce = auth_client_admin.post("/accounts/logout/")
    assert responce.status_code == 302
    
@pytest.mark.django_db
def test_player_logout(auth_client_player):
    responce = auth_client_player.post("/accounts/logout/")
    assert responce.status_code == 302