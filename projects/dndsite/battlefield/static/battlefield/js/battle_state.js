import { BattlefieldAPI } from './battlefield_api.js';

const battleState = {
    lobbyId: -1,
    lobbyData: {
        locations: [{
            characterPositions: []
        }]
    },
    selectedLocationId: -1,
    selectedLocationData: {},
    characterPositions: [],
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
        battleState.selectedLocationId = locationId;
    }

    battleState.lobbyData = await battleState.battlefieldAPI.getLobby(battleState.lobbyId);
    
    
    updateSelectedLocation(battleState.selectedLocationId);
    //battleState.characterPositions = battleState.selectedLocationData.characterPositions;
    
    return battleState;
}

export function updateSelectedLocation(newLocationId) {
    if (!newLocationId) 
        return;

    battleState.selectedLocationId = newLocationId;
    battleState.selectedLocationData = battleState.lobbyData.locations.find(loc => {
        return loc.id == battleState.selectedLocationId;
    });
    
}

export const stateReady = new Promise((resolve) => {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => resolve(initBattleState()));
    } else {
        resolve(initBattleState());
    }
});