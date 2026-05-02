export class GridMath {
    static getCellOnCords(gridCellWidth, gridCellHeight, x, y, includeLabels = false) {
        const col = Math.floor(x / gridCellWidth); 
        const row = Math.floor(y / gridCellHeight);
        return includeLabels ? [col-1, row-1] : [col, row];
    }
}

export class Vector2 {
    constructor (x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }
}

export class Vector2Math {
    static subtract(vector1, vector2) {
        return new Vector2(vector1.x - vector2.x, vector1.y - vector2.y);
    }

    static add(vector1, vector2) {
        return new Vector2(vector1.x + vector2.x, vector1.y + vector2.y);
    }

    static multiply(vector, multiplier) {
        return new Vector2(vector.x * multiplier, vector.y * multiplier);
    }
}