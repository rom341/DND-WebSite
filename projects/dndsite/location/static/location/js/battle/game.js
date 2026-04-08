import {Background} from "./background.js"
import {Player} from "./player.js"

class Game {
    constructor(context, width, height) {
        this.context = context
        this.width = width;
        this.height = height;

        this.cellWidth = 50;
        this.cellHeight = 50;

        this.background = new Background(this);
        this.player = new Player(this);
    }

    update() {

    }

    draw() {
        this.background.drawGrid(this.context);
        this.player.draw(this.context);
    }
}

function runBattleRender() {
    const canvasElement = document.getElementById("canvas1");
    const context = canvasElement.getContext("2d");
    canvasElement.width = 500;
    canvasElement.height = 500;

    const game = new Game(context, canvasElement.width, canvasElement.height);
    console.log(game);
    game.draw();
}

window.addEventListener('load', () => {
    runBattleRender()
});