import { BattlefieldAPI } from './battlefield_api.js';

const battleState = {
    lobbyId: -1,
    locationId: -1,
    characterPositions: [],
    locationData: {},
    battlefieldAPI: new BattlefieldAPI()
};

async function initBattleState() {
    const lobbyIdElement = document.getElementById('current-lobby-id');
    const lobbyId = lobbyIdElement ? JSON.parse(lobbyIdElement.textContent) : null;
    if (!lobbyId) {
        console.error("Lobby ID is missing");
    }
    else {
        battleState.lobbyId = lobbyId;
    }

    const locationIdElement = document.getElementById('current-location-id');
    const locationId = locationIdElement ? JSON.parse(locationIdElement.textContent) : null;
    if (!lobbyId) {
        console.error("Location ID is missing");
    }
    else {
        battleState.locationId = locationId;
    }

    battleState.locationData = await battleState.battlefieldAPI.getLocation(battleState.locationId);
    battleState.characterPositions = await battleState.battlefieldAPI.getCharacterPositions(battleState.lobbyId);

    return battleState;
}

export const stateReady = new Promise((resolve) => {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => resolve(initBattleState()));
    } else {
        resolve(initBattleState());
    }
});