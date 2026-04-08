import {Background} from "./background.js"
import {Character} from "./player.js"
import { stateReady } from '../../../battlefield/js/battle_state.js';

class Game {
    constructor(context, width, height, battleState) {
        this.context = context
        this.width = width;
        this.height = height;
        this.battleState = battleState;

        this.cellWidth = 50;
        this.cellHeight = 50;

        this.background = new Background(this);
        //this.player = new Character(this);
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
    }   
    
    initCharacterPositions() {
        const characterPositions = this.selectedLocationData.characterPositions;
        this.characters = characterPositions.map((data) => new Character(this, data));
    }

    onCanvasClick(clickPos){
    }
}

async function runBattleRender() {
    const canvasElement = document.getElementById("canvas1");
    const context = canvasElement.getContext("2d");
    canvasElement.width = 500;
    canvasElement.height = 500;

    const battleState = await stateReady;
    const game = new Game(context, canvasElement.width, canvasElement.height, battleState);
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