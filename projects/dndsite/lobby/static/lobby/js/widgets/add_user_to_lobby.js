import { LobbyAPI } from '../../../core/js/api/lobby.js';

async function sendAddUserToLobbyMessage() {
    const mainContainer = document.getElementById("add-user-to-lobby-widget-content");

    const lobbyIdElement = mainContainer.querySelector('[name="lobby_id"]')
    const selectedUserIdElement = mainContainer.querySelector("#id_user_id");

    await LobbyAPI.addUserToLobby(parseInt(lobbyIdElement.value), parseInt(selectedUserIdElement.value));
}

async function initAddUserToLobbyForm() {
    document.getElementById('add-user-to-lobby-widget-button').addEventListener('click', async (e) => {
        await sendAddUserToLobbyMessage();
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    await initAddUserToLobbyForm();
});