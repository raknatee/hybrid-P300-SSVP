const setBG = (ctx: CanvasRenderingContext2D,canvasWidth:number,canvasHeight:number):void => {

    ctx.fillStyle = `rgb(125,125,125)`;
    ctx.fillRect(0, 0, canvasWidth, canvasHeight);
}

export {
    setBG
}