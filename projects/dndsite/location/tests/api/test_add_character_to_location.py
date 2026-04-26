import pytest

@pytest.mark.django_db
def test_add_character_to_location(auth_admin_client, default_test_lobbys_list, default_test_characters_list, default_test_locations_list):
    test_character = default_test_characters_list[0]
    test_lobby = default_test_lobbys_list[0]
    
    payload = dict(
        lobbyId = test_lobby.id,
        characterId = test_character.id,
        locationId = default_test_locations_list[0].id,
        targetRow = 1,
        targetColumn = 2
    )
    
    responce = auth_admin_client.post("/api/location/add_character_to_location/", payload)
    
    data = responce.data
    
    characterState = test_character.states.first()
    assert responce.status_code == 200
    assert characterState != None
    assert characterState.character == test_character
    assert characterState.lobby == test_lobby