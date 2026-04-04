import { stateReady } from './battle_state.js';
import { renderBattleMap } from './battle_map.js';


// function clearCells(gridCells){
//     const marks = document.querySelectorAll('.character_mark');
//     marks.forEach(mark => mark.remove());
// }

// function addCharacterMarks(gridCells, characterPositions){
//     const gridCellsArray = Array.from(gridCells);
//     for(var i = 0; i < characterPositions.length; i++){
//         var characterPosition = characterPositions[i];
//         var CellToAddCharacter = grid.querySelector(`[data-x="${pos.column}"][data-y="${pos.row}"]`);

//         const newDiv = document.createElement('div');

//         newDiv.className = 'character_mark';
//         newDiv.textContent = characterPosition.character.character_name;
//         CellToAddCharacter.appendChild(newDiv);
//     }
// }

async function sendMoveCharacterMessageWS(socket) {
    const battleState = await stateReady;
    const target_column = document.getElementById("id_column").value;
    const target_row = document.getElementById("id_row").value;
    const target_character_id = document.getElementById("id_name").value;

    if (battleState.lobbyId != undefined && battleState.selectedLocationId != undefined && target_character_id != undefined && target_column != undefined && target_row != undefined){
        const dataToSend = JSON.stringify({
            'column': target_column,
            'row': target_row,
            'name': target_character_id,
            'current_location_id': battleState.selectedLocationId,
            'current_lobby_id': battleState.lobbyId
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

    battleState.characterPositions = data.character_positions;
    await renderBattleMap();
}

async function initWebSocket() {
    const battleState = await stateReady;
    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/battlefield/${battleState.lobbyId}/`);
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