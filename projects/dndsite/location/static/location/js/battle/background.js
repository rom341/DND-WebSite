export class Background {
    constructor(game) {
        this.game = game;
        this.cacheCanvas = document.createElement('canvas');
        this.cacheCtx = this.cacheCanvas.getContext('2d');
        this.isCached = false;

        this.gridLineWidth = 6;
        this.gridLineHeight = 6;
    }

    renderToCache() {
        this.cacheCanvas.width = this.game.canvas.width;
        this.cacheCanvas.height = this.game.canvas.height;
        
        this.drawGridLabels(this.cacheCtx);
        this.drawGrid(this.cacheCtx);
        this.isCached = true;
    }

    draw(context) {
        if (!this.isCached) {
            this.renderToCache();
        }
        context.drawImage(this.cacheCanvas, 0, 0);
    }

    drawGridLabels(context) {
        context.fillStyle = "rgba(255, 255, 255, 1)"; 
        context.font = "30px Arial"; 
        
        context.textAlign = "center";
        context.textBaseline = "middle";

        for (let row = 1; row < this.game.canvas.height / this.game.cellHeight; row++) {
            const y = row * this.game.cellHeight + this.game.cellHeight / 2;
            context.fillText(row - 1, this.game.cellWidth / 2, y);
        }

        for (let col = 1; col < this.game.canvas.width / this.game.cellWidth; col++) {
            const x = col * this.game.cellWidth + this.game.cellWidth / 2;
            context.fillText(col - 1, x, this.game.cellHeight / 2);
        }
    }

    drawGrid(context) {
        context.fillStyle = "black";
        for(var y = this.game.cellHeight; y <= this.game.canvas.height + 1; y += this.game.cellHeight) {
            context.fillRect(0, y - this.gridLineHeight / 2, this.game.canvas.width, this.gridLineHeight);
        }
        for(var x = this.game.cellWidth; x <= this.game.canvas.width + 1; x += this.game.cellWidth) {
            context.fillRect(x - this.gridLineWidth / 2, 0, this.gridLineWidth, this.game.canvas.height);
        }
    }

    getCellOnCords(x, y) {
        const col = Math.floor(x / this.game.cellWidth) - 1; 
        const row = Math.floor(y / this.game.cellHeight) - 1;        
        return [col, row];
    }
}