import pytest

@pytest.mark.django_db
def test_add_character_to_location_(auth_client_admin, default_test_lobbys_list, default_test_characters_list, default_test_locations_list):
    test_character = default_test_characters_list[0]
    test_lobby = default_test_lobbys_list[0]
    
    payload = {
        "lobbyId": test_lobby.id,
        "characterId": test_character.id,
        "locationId": default_test_locations_list[0].id,
        "targetRow": 1,
        "targetColumn": 2
    }
    
    responce = auth_client_admin.post("/api/location/add_character", payload, format="json")
        
    character_state = test_character.states.first()
    assert responce.status_code == 200
    assert character_state != None
    assert character_state.character == test_character
    assert character_state.lobby == test_lobby