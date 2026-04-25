import { apiRequest } from './base.js';

export const LobbyAPI = {
    // getPlayers: (lobbyId) => apiRequest(`/api/lobby/${lobbyId}/players/`),
    
    // createLobby: (name) => apiRequest('/api/lobby/create/', 'POST', { name }),

    addUserToLobby: (lobbyId, userId) => apiRequest('/api/lobby/add_user_to_lobby/', 'POST', {
        "lobbyId": lobbyId,
        "selectedUserId": userId
    }),
    
    addCharacterToLobby: (characterId, lobbyId, targetRow, targetColumn) => apiRequest(
        '/api/lobby/add_character_to_lobby/', 
        'POST', 
        {
            "characterId": characterId,
            "lobbyId": lobbyId,
            "targetRow": targetRow,
            "targetColumn": targetColumn
        }
    )
};