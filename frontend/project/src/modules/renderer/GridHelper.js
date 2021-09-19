class GridHelper {
    constructor(x, y, numCol, sizeX, sizeY, rowGap = 0, colGap = 0) {
        this.x = x
        this.y = y
        this.numCol = numCol
        this.sizeX = sizeX
        this.sizeY = sizeY
        this.rowGap = rowGap
        this.colGap = colGap

    }
    getCoordinate(index) {
        let posIX = index % this.numCol
        let posIY = Math.floor(index / this.numCol)
        let startX = posIX * (this.sizeX + this.rowGap)
        let startY = posIY * (this.sizeY + this.colGap)
        return { 'x': startX + this.x, 'y': startY + this.y }
    }
}

export { GridHelper }