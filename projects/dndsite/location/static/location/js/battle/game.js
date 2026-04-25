import {Background} from "./background.js"
import {Character} from "./character.js"
import {SelectCharacterController} from "../widgets/battle_map_character_selector.js"
import { stateReady } from '../../../battlefield/js/battle_state.js';
import { BattleMediator } from "../services/battle_mediator.js";
import { SocketService } from "../services/socket_service.js";
import {sendMoveCharacterMessageWS} from "../widgets/move_character_web_socket.js"


class Game {
    constructor(canvasElement, width, height, cellWidth, cellHeight, battleState) {
        this.canvas = canvasElement
        this.context = this.canvas.getContext("2d");
        this.width = width;
        this.height = height;
        this.battleState = battleState;
        
        this.cellWidth = cellWidth;
        this.cellHeight = cellHeight;
        
        this.updateLocationData();
        this.updateCharacterPositions();
        this.initBackground();
        this.initControllers();
    }
    
    update() {
        this.draw();
    }
    
    draw() {
        this.context.clearRect(0, 0, this.width, this.height);
        this.background.draw(this.context);
        this.characters.forEach(char => char.draw(this.context));
    }
    
    updateLocationData() {
        this.selectedLocationData = this.battleState.selectedLocationData;
    }
    
    initBackground() {
        this.background = new Background(this, this.selectedLocationData);
    }
    
    updateCharacterPositions() {
        const characterPositions = this.selectedLocationData.characterPositions;
        this.characters = characterPositions.map((characterPosition) => new Character(this, characterPosition));
    }
    
    initControllers() {
        const socketService = new SocketService(`ws://127.0.0.1:8000/ws/battlefield/${this.battleState.lobbyData.id}/`);
        socketService.connect();
        this.mediator =  new BattleMediator(this, socketService);
        this.characterSellectController = new SelectCharacterController();
    }
    
    notifyCharacterMove(characterId, targetRow, targetColumn) {
        this.mediator.handleUserAction("REQUEST_MOVE", {
            name: characterId,
            current_location_id: this.selectedLocationData.id,
            row: targetRow, 
            column: targetColumn
        });
    }

    onCanvasClick(e) {
        const canvasBounds = this.canvas.getBoundingClientRect();
        const scaleX = this.canvas.width / canvasBounds.width;
        const scaleY = this.canvas.height / canvasBounds.height;
        
        const clickPos = {
            x: (e.clientX - canvasBounds.left) * scaleX,
            y: (e.clientY - canvasBounds.top) * scaleY
        };

        const [col, row] = this.background.getCellOnCords(clickPos.x, clickPos.y);    
        this.characterSellectController.updateCoords(col, row);
        
        const characterOnPosition = this.selectedLocationData.characterPositions.find(pos => 
            Number(pos.column) === col && Number(pos.row) === row
        );
        
        if (characterOnPosition) {
            this.characterSellectController.setCharacter(characterOnPosition.id);
        }
    }

    onCanvasMouseWheel(e){
        const direction = Math.sign(e.deltaY);
    }
}

async function runBattleRender() {
    const battleState = await stateReady;
    const canvasElement = document.getElementById("canvas1");

    const cellWidth = 100;
    const cellHeight = 100;

    canvasElement.width = (battleState.selectedLocationData.columnsCount + 1) * cellWidth; //+1 for labels
    canvasElement.height = (battleState.selectedLocationData.rowsCount + 1) * cellHeight; //+1 for labels
    const game = new Game(canvasElement, canvasElement.width, canvasElement.height, cellWidth, cellHeight, battleState);    
    
    canvasElement.addEventListener('click', (e) => {
        game.onCanvasClick(e);
    });
    
    canvasElement.addEventListener('wheel', (e) => {
        e.preventDefault();
        game.onCanvasMouseWheel(e);
    }, { passive: false });

    document.getElementById('move-character-button').addEventListener('click', async (e) => {
        e.preventDefault();
        const battleState = await stateReady;
        const selectedCharacterId = game.characterSellectController.getSelectedCharacterId();
        const selectedCharacter = battleState.selectedLocationData.characterPositions.find(p => p.character.id === selectedCharacterId);
        const selectedCell = game.characterSellectController.getSelectedCords();
        if (selectedCharacterId) {
            game.notifyCharacterMove(
                selectedCharacter.id,
                selectedCell[1],
                selectedCell[0]
            )
        } else {
            console.warn("Character must be selected");
        }
    });

    game.draw();
}

window.addEventListener('load', async () => {
    await runBattleRender()
});