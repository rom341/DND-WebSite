import { BattlefieldAPI } from './battlefield_api.js';

const lobbyData = document.getElementById('current-lobby-id');
const lobbyId = lobbyData ? JSON.parse(lobbyData.textContent) : null;
if (!lobbyId) {
    console.error("Lobby ID is missing");
}

const locationData = document.getElementById('current-lobby-id');
const locationId = lobbyData ? JSON.parse(lobbyData.textContent) : null;

const socket = new WebSocket(`ws://127.0.0.1:8000/ws/battlefield/${lobbyId}/`);
console.log("Connected to ws");

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
        newDiv.textContent = characterPosition.character;
        CellToAddCharacter.appendChild(newDiv);
    }
}

function drawBattleMap(characterPositions){
    const grid = document.getElementById("grid-map");
    const gridCells = grid.children;

    const battlefieldAPI = new BattlefieldAPI();
    
    //Clear all
    clearCells(gridCells);
    //Add characters
    addCharacterMarks(gridCells, characterPositions)
}

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    drawBattleMap(data.character_positions);
};

function sendMessage() {
    const target_column = document.getElementById("id_column").value;
    const target_row = document.getElementById("id_row").value;
    const target_character_id = document.getElementById("id_name").value;

    socket.send(JSON.stringify({
        'column': target_column,
        'row': target_row,
        'name': target_character_id,
        'current_location_id': locationId,
        'current_lobby_id': lobbyId
    }));
}

document.getElementById('move-character-button').addEventListener('click', (e) => {
    e.preventDefault(); 
    sendMessage();
});