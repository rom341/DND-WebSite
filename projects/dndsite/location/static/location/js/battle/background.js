export class Background {
    constructor(game, location) {
        this.game = game;
        this.location = location;


        this.gridLineWidth = 6;
        this.gridLineHeight = 6;
    }

    update() {

    }

    draw(context) {
        this.drawGridLabels(context);
        this.drawGrid(context);
    }

    drawGridLabels(context) {
        context.fillStyle = "rgba(255, 255, 255, 1)"; 
        context.font = "30px Arial"; 
        
        context.textAlign = "center";
        context.textBaseline = "middle";

        for (let row = 1; row < this.game.height / this.game.cellHeight; row++) {
            const y = row * this.game.cellHeight + this.game.cellHeight / 2;
            context.fillText(row - 1, this.game.cellWidth / 2, y);
        }

        for (let col = 1; col < this.game.width / this.game.cellWidth; col++) {
            const x = col * this.game.cellWidth + this.game.cellWidth / 2;
            context.fillText(col - 1, x, this.game.cellHeight / 2);
        }
    }

    drawGrid(context) {
        context.fillStyle = "black";
        for(var y = this.game.cellHeight; y <= this.game.height + 1; y += this.game.cellHeight) {
            context.fillRect(0, y - this.gridLineWidth / 2, this.game.width, this.gridLineHeight);
        }
        for(var x = this.game.cellHeight; x <= this.game.width + 1; x += this.game.cellWidth) {
            context.fillRect(x - this.gridLineHeight / 2, 0, this.gridLineWidth, this.game.height);
        }
    }
}