import { apiRequest } from './base.js';

export const LobbyAPI = {
    // getPlayers: (lobbyId) => apiRequest(`/api/lobby/${lobbyId}/players/`),
    
    // createLobby: (name) => apiRequest('/api/lobby/create/', 'POST', { name }),

    addUserToLobby: (lobbyId, userId) => apiRequest('/api/lobby/add_user_to_lobby/', 'POST', {
        "lobbyId": lobbyId,
        "selectedUserId": userId
    }).data,
    
    addCharacterToLocation: (characterId, lobbyId, locationId, targetRow, targetColumn) => apiRequest(
        '/api/location/add_character_to_location/', 
        'POST', 
        {
            "characterId": characterId,
            "lobbyId": lobbyId,
            "locationId": locationId,
            "targetRow": targetRow,
            "targetColumn": targetColumn
        }
    ).data
};