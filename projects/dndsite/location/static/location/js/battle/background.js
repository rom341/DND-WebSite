export class Background {
    constructor(game) {
        this.game = game;
        this.gridLineWidth = 6;
        this.gridLineHeight = 6;
    }

    update() {

    }

    drawGrid(context) {
        context.fillStyle = "black";
        for(var y = this.game.cellHeight; y < this.game.height; y += this.game.cellHeight) {
            context.fillRect(0, y - this.gridLineWidth / 2, this.game.width, this.gridLineHeight);
        }
        for(var x = this.game.cellWidth; x < this.game.width; x += this.game.cellWidth) {
            context.fillRect(x - this.gridLineHeight / 2, 0, this.gridLineWidth, this.game.height);
        }
    }
}