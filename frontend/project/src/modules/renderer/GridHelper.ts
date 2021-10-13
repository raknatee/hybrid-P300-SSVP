class Vector2{
    x:number
    y:number
    constructor(x:number,y:number){
        this.x=x
        this.y=y
    }
}

class GridHelper {
    x:number
    y:number
    numCol:number
    sizeX:number
    sizeY:number
    rowGap:number
    colGap:number
    constructor(x:number, y:number, numCol:number, sizeX:number, sizeY:number, rowGap = 0, colGap = 0) {
        this.x = x
        this.y = y
        this.numCol = numCol
        this.sizeX = sizeX
        this.sizeY = sizeY
        this.rowGap = rowGap
        this.colGap = colGap

    }
    getCoordinate(index:number):Vector2 {
        const posIX = index % this.numCol
        const posIY = Math.floor(index / this.numCol)
        const startX = posIX * (this.sizeX + this.rowGap)
        const startY = posIY * (this.sizeY + this.colGap)
        return new Vector2(startX+this.x,startY+this.y)
        
    }
}

export { GridHelper }