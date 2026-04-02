import { BattlefieldAPI } from './battlefield_api.js';

export const battleState = {
    lobbyId: -1,
    locationId: -1,
    characterPositions: [],
    battlefieldAPI: new BattlefieldAPI()
};

const lobbyData = document.getElementById('current-lobby-id');
const lobbyId = lobbyData ? JSON.parse(lobbyData.textContent) : null;
if (!lobbyId) {
    console.error("Lobby ID is missing");
}
else {
    battleState.lobbyId = lobbyId;
}

const locationData = document.getElementById('current-lobby-id');
const locationId = locationData ? JSON.parse(locationData.textContent) : null;
if (!lobbyId) {
    console.error("Location ID is missing");
}
else {
    battleState.locationId = locationId
}




