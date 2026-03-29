import { BattlefieldAPI } from './battlefield_api.js';

const MapFormController = {
    inputs: {
        column: document.getElementById('id_column'),
        row: document.getElementById('id_row'),
        characterName: document.getElementById('id_name')
    },

    updateCoords(column, row) {
        if (this.inputs.column) this.inputs.column.value = column;
        if (this.inputs.row) this.inputs.row.value = row;
    },

    setCharacter(id) {
        if (this.inputs.characterName) this.inputs.characterName.value = id || "";
    }
};

document.addEventListener('click', async (event) => {
    const cell = event.target.closest('.grid-cell');
    const map = event.target.closest('#battle-map');
    if (!cell || !map) return;
    
    const lobbyData = document.getElementById('current-lobby-id');
    const lobbyId = lobbyData ? JSON.parse(lobbyData.textContent) : null;
    
    if (!lobbyId) {
        console.error("Lobby ID is missing");
        return;
    }
    
    const column = parseInt(cell.dataset.x, 10);
    const row = parseInt(cell.dataset.y, 10);
    
    MapFormController.updateCoords(column, row);
    
    const battlefieldAPI = new BattlefieldAPI();
    const positions = await battlefieldAPI.getCharacterPositions(lobbyId);
    
    const found_position = positions.find(pos => 
        Number(pos.column) === column && Number(pos.row) === row
    );
    
    MapFormController.setCharacter(found_position ? found_position.character : null);
});
