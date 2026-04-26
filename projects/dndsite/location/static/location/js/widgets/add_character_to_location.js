import { LobbyAPI } from '../../../core/js/api/lobby.js';

async function sendAddcharacterToLocationMessage() {
    const mainContainer = document.getElementById("add-character-to-location-widget-content");

    const lobbyIdElement = mainContainer.querySelector('[name="lobby_id"]')
    const selectedCharacterIdElement = mainContainer.querySelector("#id_character_id");
    const selectedLocationIdElement = mainContainer.querySelector("#id_location_id");
    const selectedRowElement = mainContainer.querySelector("#id_target_row");
    const selectedColumnElement = mainContainer.querySelector("#id_target_column");

    await LobbyAPI.addCharacterToLocation(
        parseInt(selectedCharacterIdElement.value),
        parseInt(lobbyIdElement.value),
        parseInt(selectedLocationIdElement.value),
        parseInt(selectedRowElement.value),
        parseInt(selectedColumnElement.value)    
    );
}

async function initAddCharacterToLocationForm() {
    document.getElementById('add-character-to-location-widget-button').addEventListener('click', async (e) => {
        await sendAddcharacterToLocationMessage();
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    await initAddCharacterToLocationForm();
});