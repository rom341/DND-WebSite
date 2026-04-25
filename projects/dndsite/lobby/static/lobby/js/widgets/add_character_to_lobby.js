import { LobbyAPI } from '../../../core/js/api/lobby.js';

async function sendAddcharacterToLobbyMessage() {
    const mainContainer = document.getElementById("add-character-to-lobby-widget-content");

    const lobbyIdElement = mainContainer.querySelector('[name="lobby_id"]')
    const selectedCharacterIdElement = mainContainer.querySelector("#id_character_id");
    const selectedLocationIdElement = mainContainer.querySelector("#id_location_id");
    const selectedRowElement = mainContainer.querySelector("#id_target_row");
    const selectedColumnElement = mainContainer.querySelector("#id_target_column");

    await LobbyAPI.addUserToLobby(
        parseInt(selectedCharacterIdElement.value),
        parseInt(lobbyIdElement.value),
        parseInt(selectedRowElement.value),
        parseInt(selectedColumnElement.value)    
    );
}

async function initAddCharacterToLobbyForm() {
    document.getElementById('add-character-to-lobby-widget-button').addEventListener('click', async (e) => {
        await sendAddcharacterToLobbyMessage();
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    await initAddCharacterToLobbyForm();
});