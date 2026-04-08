export class Background {
    constructor(game, location) {
        this.game = game;
        this.location = location;
        this.gridLineWidth = 6;
        this.gridLineHeight = 6;
    }

    update() {

    }

    drawGrid(context) {
        context.fillStyle = "black";
        for(var y = 0; y <= this.game.height; y += this.game.cellHeight) {
            context.fillRect(0, y - this.gridLineWidth / 2, this.game.width, this.gridLineHeight);
        }
        for(var x = 0; x <= this.game.width; x += this.game.cellWidth) {
            context.fillRect(x - this.gridLineHeight / 2, 0, this.gridLineWidth, this.game.height);
        }
    }
}