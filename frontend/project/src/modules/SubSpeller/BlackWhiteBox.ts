enum BoxColor{
    BLACK="BLACK",
    WHITE="WHITE"
}

class Box{
    imageData:ImageData
    ctx:CanvasRenderingContext2D
    constructor(ctx:CanvasRenderingContext2D,width:number,height:number,color:BoxColor){
        this.ctx = ctx
        this.imageData = this.ctx.createImageData(width,height)
        const buf = new Uint32Array(this.imageData.data.buffer)
        let i=0
        for(let y=0;y<height;y++){
            for(let x=0;x<width;x++){
                if(color==BoxColor.BLACK){
                    buf[i] = 0xFFFFFFFF 
                }
                if(color==BoxColor.WHITE){
                    buf[i] = 0xFF000000
                }
                i++
            }
        }
    }
    fill(x:number,y:number):void{
        this.ctx.putImageData(this.imageData,x,y)
    }
}

export {Box,BoxColor}