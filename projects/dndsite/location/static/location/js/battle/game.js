import {Background} from "./background.js"
import {Character} from "./player.js"
import { stateReady } from '../../../battlefield/js/battle_state.js';

class Game {
    constructor(context, width, height, cellWidth, cellHeight, battleState) {
        this.context = context
        this.width = width;
        this.height = height;
        this.battleState = battleState;

        this.cellWidth = cellWidth;
        this.cellHeight = cellHeight;

        this.initLocationData();
        this.initCharacterPositions();
    }

    update() {

    }

    draw() {
        this.context.clearRect(0, 0, this.width, this.height);
        this.background.drawGrid(this.context);
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

    onCanvasClick(clickPos){
    }
}

async function runBattleRender() {
    const battleState = await stateReady;
    const canvasElement = document.getElementById("canvas1");
    const context = canvasElement.getContext("2d");

    const cellWidth = 50;
    const cellHeight = 50;

    canvasElement.width = (battleState.selectedLocationData.columnsCount) * cellWidth;
    canvasElement.height = (battleState.selectedLocationData.rowsCount) * cellHeight;
    const game = new Game(context, canvasElement.width, canvasElement.height, cellWidth, cellHeight, battleState);

    
    console.log(game);
    game.draw();

    canvasElement.addEventListener('click', (e) => {
        const canvasAbsolutePos = canvasElement.getBoundingClientRect();
        const clickPos = {
            x: Math.round(e.clientX - canvasAbsolutePos.left),
            y: Math.round(e.clientY - canvasAbsolutePos.top)
        };
        game.onCanvasClick(clickPos);
    });
}

window.addEventListener('load', async () => {
    await runBattleRender()
});