import { stateReady, updateLocationData } from '../../../battlefield/js/battle_state.js';

async function sendLocationCreateMessage() {
    console.log("t");
    const battleState = await stateReady;
    const mainContainer = document.getElementById("create-location-widget-content");

    const locationNameElement = mainContainer.querySelector("#id_name");
    const locationDescriptionElement = mainContainer.querySelector("#id_description");
    const locationRowsCountElement = mainContainer.querySelector("#id_rows_count");
    const locationColumnsCountElement = mainContainer.querySelector("#id_columns_count");

    const newLocationData = {
        lobbyId: battleState.lobbyData.id,
        locationName: locationNameElement.value,
        locationDescription: locationDescriptionElement.value,
        locationRowsCount: parseInt(locationRowsCountElement.value),
        locationColumnsCount: parseInt(locationColumnsCountElement.value)
    };

    const createdLocationData = await battleState.battlefieldAPI.createLocation(newLocationData);
    updateLocationData(createdLocationData);
}

async function initCreateLocationForm() {
    document.getElementById('create-location-widget-button').addEventListener('click', async (e) => {
        await sendLocationCreateMessage();
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    await initCreateLocationForm();
});