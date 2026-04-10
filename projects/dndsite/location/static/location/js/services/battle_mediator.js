import { stateReady, updateLocationData } from '../../../battlefield/js/battle_state.js';

export class BattleMediator {
    constructor (game, socketService) {
        this.game = game;
        this.socketService = socketService;
        
        this.bindEvents();
    }

    bindEvents() {
        this.socketService.subscribe("CHARACTER_MOVED", async (data) => {
            const battleState = await stateReady;
            updateLocationData(data);
            this.game.updateLocationData();
            this.game.updateCharacterPositions();
            this.game.draw();
        });

        this.game.onActionRequested = (type, data) => {
            this.handleUserAction(type, data);
        };
    }

    handleUserAction(type, data) {        
        if (type === 'REQUEST_MOVE') {
            this.socketService.send('REQUEST_MOVE', data);
        }
    }
}