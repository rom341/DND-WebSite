import { stateReady, updateLocationData } from '../../../battlefield/js/battle_state.js';
import { renderBattleMap } from './battle_map.js';

async function sendMoveCharacterMessageWS(socket) {
    const battleState = await stateReady;
    const target_column = document.getElementById("id_column").value;
    const target_row = document.getElementById("id_row").value;
    const target_character_id = document.getElementById("id_name").value;

    if (battleState.lobbyData.id != undefined && battleState.selectedLocationData.id != undefined && target_character_id != undefined && target_column != undefined && target_row != undefined){
        const dataToSend = JSON.stringify({
            'column': target_column,
            'row': target_row,
            'name': target_character_id,
            'current_location_id': battleState.selectedLocationData.id,
            'current_lobby_id': battleState.lobbyData.id
        });
        socket.send(dataToSend);
    }
    else {
        console.error("Cant move character. Wrong input data")
    }
}

async function onMessageCallback(e) {
    const battleState = await stateReady;
    const data = JSON.parse(e.data); 

    updateLocationData(data);
    await renderBattleMap();
}

async function initWebSocket() {
    const battleState = await stateReady;
    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/battlefield/${battleState.lobbyData.id}/`);
    socket.onmessage = onMessageCallback;
    return socket;
}

document.addEventListener('DOMContentLoaded', async () => {
    const webSocket = await initWebSocket()

    document.getElementById('move-character-button').addEventListener('click', async (e) => {
        e.preventDefault(); 
        await sendMoveCharacterMessageWS(webSocket);
    });
});