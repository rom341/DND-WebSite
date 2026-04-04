import { BattlefieldAPI } from './battlefield_api.js';

const battleState = {
    lobbyData: {
        id: -1,
        locations: [{
            characterPositions: []
        }]
    },
    selectedLocationData: {
        id: -1,
        characterPositions: []
    },
    battlefieldAPI: new BattlefieldAPI()
};

function mapLocationData(rawLoc) {
    if (!rawLoc) return null;
    return {
        ...rawLoc,
        characterPositions: rawLoc.character_positions || [],
        rowsCount: rawLoc.rows_count,
        columnsCount: rawLoc.columns_count,

        character_positions: undefined,
        rows_count: undefined,
        columns_count: undefined
    };
}

async function initBattleState() {
    const lobbyIdElement = document.getElementById('current-lobby-id');
    const lobbyId = lobbyIdElement ? JSON.parse(lobbyIdElement.textContent) : null;
    if (!lobbyId) {
        console.error("Lobby ID is missing");
        return;
    }

    const locationIdElement = document.getElementById('current-location-id');
    const locationId = locationIdElement ? JSON.parse(locationIdElement.textContent) : null;
    if (!locationId) {
        console.error("Location ID is missing");
        return;
    }

    const rawLobbyData = await battleState.battlefieldAPI.getLobby(lobbyId);
    if (rawLobbyData && rawLobbyData.locations) {
        rawLobbyData.locations = rawLobbyData.locations.map(mapLocationData);
    }
    battleState.lobbyData = rawLobbyData;
    
    
    updateSelectedLocation(locationId);
    return battleState;
}

export function updateSelectedLocation(newLocationId) {
    if (!newLocationId) 
        return;

    battleState.selectedLocationData = battleState.lobbyData.locations.find(loc => {
        return loc.id == newLocationId;
    });    
}

export function updateLocationData(rawLocationData) {
    if (!rawLocationData || !rawLocationData.id) return;

    const updatedLocation = mapLocationData(rawLocationData);
    const index = battleState.lobbyData.locations.findIndex(loc => loc.id === updatedLocation.id);

    if (index !== -1) {
        battleState.lobbyData.locations[index] = updatedLocation;
        if (battleState.selectedLocationData && battleState.selectedLocationData.id === updatedLocation.id) {
            battleState.selectedLocationData = updatedLocation;
        }
        
        //console.log(`Location ${updatedLocation.id} updated successfully.`);
    } else {
        //console.warn(`Location with id ${updatedLocation.id} not found in lobbyData.`);
    }
}

export const stateReady = new Promise((resolve) => {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => resolve(initBattleState()));
    } else {
        resolve(initBattleState());
    }
});