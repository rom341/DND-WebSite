import { battleState } from './battle_state.js';

const socket = new WebSocket(`ws://127.0.0.1:8000/ws/battlefield/${battleState.lobbyId}/`);

function clearCells(gridCells){
    for(var i = 0; i < gridCells.length; i++){
        var gridCell = gridCells[i];
        gridCell.innerHTML = '';
    }
}

function addCharacterMarks(gridCells, characterPositions){
    const gridCellsArray = Array.from(gridCells);
    for(var i = 0; i < characterPositions.length; i++){
        var characterPosition = characterPositions[i];
        var CellToAddCharacter = gridCellsArray.filter(element => element.dataset.x == characterPosition.column && element.dataset.y == characterPosition.row)[0];

        const newDiv = document.createElement('div');

        newDiv.className = 'character_mark';
        newDiv.textContent = characterPosition.character.character_name;
        CellToAddCharacter.appendChild(newDiv);
    }
}

async function drawBattleMap(characterPositions){
    const grid = document.getElementById("grid-map");
    const gridCells = grid.children;
    
    //Clear all
    clearCells(gridCells);
    //Add characters
    addCharacterMarks(gridCells, characterPositions)
}

socket.onmessage = async function(e) {
    const data = JSON.parse(e.data);
    battleState.characterPositions = data.character_positions;  
    await drawBattleMap(data.character_positions);
};

function sendMoveCharacterMessageWS() {
    const target_column = document.getElementById("id_column").value;
    const target_row = document.getElementById("id_row").value;
    const target_character_id = document.getElementById("id_name").value;

    if (battleState.lobbyId != undefined && battleState.locationId != undefined && target_character_id != undefined && target_column != undefined && target_row != undefined){
        const dataToSend = JSON.stringify({
            'column': target_column,
            'row': target_row,
            'name': target_character_id,
            'current_location_id': battleState.locationId,
            'current_lobby_id': battleState.lobbyId
        });
        socket.send(dataToSend);
    }
    else {
        console.error("Cant move character. Wrong input data")
    }
}

document.getElementById('move-character-button').addEventListener('click', (e) => {
    e.preventDefault(); 
    sendMoveCharacterMessageWS();
});