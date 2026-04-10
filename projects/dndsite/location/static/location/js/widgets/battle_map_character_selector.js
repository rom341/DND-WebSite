import { stateReady } from '../../../battlefield/js/battle_state.js';

export class SelectCharacterController {
    constructor () {
        this.inputs = {
            columnInputElement: document.getElementById('id_column'),
            rowInputElement: document.getElementById('id_row'),
            characterInputElement: document.getElementById('id_name')
        };
    }

    updateCoords(column, row) {
        if (this.inputs.columnInputElement) this.inputs.columnInputElement.value = column;
        if (this.inputs.rowInputElement) this.inputs.rowInputElement.value = row;
    }

    getSelectedCords() {
        return [
            Number(this.inputs.columnInputElement.value),
            Number(this.inputs.rowInputElement.value)
        ]
    }

    setCharacter(id) {
        if (this.inputs.characterInputElement) this.inputs.characterInputElement.value = id || "";
    }

    getSelectedCharacterId() {
        return Number(this.inputs.characterInputElement.value);
    }
};