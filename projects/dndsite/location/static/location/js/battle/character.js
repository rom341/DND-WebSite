import { stateReady } from '../../../battlefield/js/battle_state.js';

export class Character {
    constructor(game, characterPosition) {
        this.game = game;
        this.id = characterPosition.character;
        this.row = characterPosition.row;
        this.column = characterPosition.column;

        this.sourceSpriteWidth = 100;
        this.sourceSpriteHeight = 200;
        this.destinationSpriteWidth = game.cellWidth / 2;
        this.destinationSpriteHeight = game.cellHeight;

        this.rowShift = 1;
        this.columnShift = 1;

        this.playerSpriteSheetElement = document.getElementById("player-sprite-sheet");
    }

    update() {

    }

    draw(context) {
        const columnPosX = (this.column + this.columnShift) * this.game.cellWidth;
        const rowPosY = (this.row + this.rowShift) * this.game.cellHeight;

        context.fillStyle = "red";
        context.fillRect(columnPosX, rowPosY, this.game.cellWidth, this.game.cellHeight);

        const centerX = columnPosX + (this.game.cellWidth - this.destinationSpriteWidth) / 2;
        const centerY = rowPosY + (this.game.cellHeight - this.destinationSpriteHeight) / 2;

        context.drawImage(
            this.playerSpriteSheetElement,
            0, 0, 
            this.sourceSpriteWidth, this.sourceSpriteHeight,
            centerX, centerY, 
            this.destinationSpriteWidth, this.destinationSpriteHeight
        ); 
    }


}