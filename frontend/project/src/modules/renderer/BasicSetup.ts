const setBG = (_this:any):void => {

    _this.ctx.fillStyle = "white";
    _this.ctx.fillRect(0, 0, _this.canvas.width, _this.canvas.height);
}

export {
    setBG
}