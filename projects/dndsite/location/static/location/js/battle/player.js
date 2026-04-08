export class Player {
    constructor(game) {
        this.game = game;
        this.sourceSpriteWidth = 100;
        this.sourceSpriteHeight = 200;
        this.posX = 0;
        this.posY = 0;
        this.destinationSpriteWidth = 25;
        this.destinationSpriteHeight = 50;

        this.playerSpriteSheetElement = document.getElementById("player-sprite-sheet");
    }

    update() {

    }

    draw(context) {
        context.fillStyle = "red";
        context.fillRect(this.posX, this.posY, this.game.cellWidth, this.game.cellHeight);
        
        context.drawImage(
            this.playerSpriteSheetElement, //sprite sheet to use
            0, 0, //sprite pos on sprite sheet
            this.sourceSpriteWidth, this.sourceSpriteHeight, //sprite size on sprite sheet
            this.posX + this.destinationSpriteWidth / 2, this.posY, //where to draw on context
            this.destinationSpriteWidth, this.destinationSpriteHeight //size that will be consumed by img. if it is different from sprite size, img will be squeezed
        ); 
    }
}