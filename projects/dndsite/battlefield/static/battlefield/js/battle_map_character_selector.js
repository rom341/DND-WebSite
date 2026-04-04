import { stateReady } from './battle_state.js';

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
    const battleState = await stateReady;
    const cell = event.target.closest('.grid-cell');
    const map = event.target.closest('#battle-map');
    if (!cell || !map) return;
       
    if (!battleState.lobbyId) {
        console.error("Lobby ID is missing");
        return;
    }
    
    const column = parseInt(cell.dataset.x, 10);
    const row = parseInt(cell.dataset.y, 10);
    
    MapFormController.updateCoords(column, row);
    
    //const positions = await battlefieldAPI.getCharacterPositions(lobbyId);
    const positions = battleState.characterPositions;
    
    const found_position = positions.find(pos => 
        Number(pos.column) === column && Number(pos.row) === row
    );
    if (found_position) {
        MapFormController.setCharacter(found_position.character.id);
    }
});
