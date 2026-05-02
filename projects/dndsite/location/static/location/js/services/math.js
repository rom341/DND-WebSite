export class GridMath {
    static getCellOnCords(gridCellWidth, gridCellHeight, x, y, includeLabels = false) {
        const col = Math.floor(x / gridCellWidth); 
        const row = Math.floor(y / gridCellHeight);
        return includeLabels ? [col-1, row-1] : [col, row];
    }
}