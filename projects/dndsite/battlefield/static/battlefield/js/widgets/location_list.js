import { stateReady, updateSelectedLocation } from '../battle_state.js';
import { renderBattleMap } from './battle_map.js';

async function onLocationSelectChange(event) {
    updateSelectedLocation(parseInt(event.target.value));
    await renderBattleMap();
}

export async function renderLocationList() {
    const battleState = await stateReady;
    const mainContainer = document.getElementById("location-list-content");
    const locationSelectTemplate = document.getElementById("location-select-template");
    const locationSelectInstance = locationSelectTemplate.content.cloneNode(true).querySelector('#location-select');

    const locationSelectOptionTemplate = document.getElementById("location-select-option-template");
    
    const locations = await battleState.battlefieldAPI.getLocationsForLobby(battleState.lobbyData.id);
    
    locations.forEach((location) => {
        const locationSelectOptionInstance = locationSelectOptionTemplate.content.cloneNode(true).querySelector('.location-select-option');
        locationSelectOptionInstance.textContent = `${location.name} (${location.rows_count}X${location.columns_count})`;
        locationSelectOptionInstance.value = location.id;

        locationSelectInstance.appendChild(locationSelectOptionInstance);
    });

    locationSelectInstance.addEventListener('change', (event) => {
        onLocationSelectChange(event);
    });
    mainContainer.appendChild(locationSelectInstance);
}

document.addEventListener('DOMContentLoaded', async () => {
    await renderLocationList();
});

