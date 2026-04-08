import { stateReady } from '../../../battlefield/js/battle_state.js';

export class Character {
    constructor(game, characterPosition) {
        this.game = game;
        this.id = characterPosition.character;
        this.row = characterPosition.row;
        this.column = characterPosition.column;

        this.sourceSpriteWidth = 100;
        this.sourceSpriteHeight = 200;
        this.destinationSpriteWidth = 25;
        this.destinationSpriteHeight = 50;

        this.playerSpriteSheetElement = document.getElementById("player-sprite-sheet");
    }

    update() {

    }

    draw(context) {
        const columnPosX = this.column * this.game.cellWidth;
        const rowPosY = this.row * this.game.cellHeight;

        context.fillStyle = "red";
        context.fillRect(columnPosX, rowPosY, this.game.cellWidth, this.game.cellHeight);

        context.drawImage(
            this.playerSpriteSheetElement, //sprite sheet to use
            0, 0, //sprite pos on sprite sheet
            this.sourceSpriteWidth, this.sourceSpriteHeight, //sprite size on sprite sheet
            columnPosX + this.destinationSpriteWidth / 2, rowPosY, //where to draw on context
            this.destinationSpriteWidth, this.destinationSpriteHeight //size that will be consumed by img. if it is different from sprite size, img will be squeezed
        ); 
    }


}