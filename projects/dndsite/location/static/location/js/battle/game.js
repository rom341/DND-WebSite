import {Background} from "./background.js"
import {Character} from "./character.js"
import {SelectCharacterController as CharacterSellectController} from "../widgets/battle_map_character_selector.js"
import { stateReady } from '../../../battlefield/js/battle_state.js';

class Game {
    constructor(canvasElement, width, height, cellWidth, cellHeight, battleState) {
        this.canvasElement = canvasElement
        this.context = this.canvasElement.getContext("2d");
        this.width = width;
        this.height = height;
        this.battleState = battleState;

        this.cellWidth = cellWidth;
        this.cellHeight = cellHeight;

        this.initLocationData();
        this.initCharacterPositions();
        this.initControllers();
    }

    update() {

    }

    draw() {
        this.context.clearRect(0, 0, this.width, this.height);
        this.background.draw(this.context);
        this.characters.forEach(char => char.draw(this.context));
    }

    initLocationData() {
        this.selectedLocationData = this.battleState.selectedLocationData;
        this.background = new Background(this, this.selectedLocationData);
    }   
    
    initCharacterPositions() {
        const characterPositions = this.selectedLocationData.characterPositions;
        this.characters = characterPositions.map((characterPosition) => new Character(this, characterPosition));
    }

    initControllers() {
        this.characterSellectController = new CharacterSellectController();
    }

onCanvasClick(e) {
const canvasBounds = this.canvasElement.getBoundingClientRect();
    const scaleX = this.canvasElement.width / canvasBounds.width;
    const scaleY = this.canvasElement.height / canvasBounds.height;

    const clickPos = {
        x: (e.clientX - canvasBounds.left) * scaleX,
        y: (e.clientY - canvasBounds.top) * scaleY
    };

    const [col, row] = this.background.getCellOnCords(clickPos.x, clickPos.y);    
    this.characterSellectController.updateCoords(col, row);
    
    const charactersOnPosition = this.selectedLocationData.characterPositions.find(pos => 
        Number(pos.column) === col && Number(pos.row) === row
    );
    
    if (charactersOnPosition) {
        this.characterSellectController.setCharacter(charactersOnPosition.id);
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
    console.log(game);
    
    canvasElement.addEventListener('click', (e) => {
        game.onCanvasClick(e);
    });
    
    canvasElement.addEventListener('wheel', (e) => {
        e.preventDefault();
        game.onCanvasMouseWheel(e);
    }, { passive: false });


    game.draw();
}

window.addEventListener('load', async () => {
    await runBattleRender()
});