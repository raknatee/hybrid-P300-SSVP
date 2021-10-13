import { getSizeW, getSizeH } from "@/modules/renderer/Sizing.js";


class UserText{
    static render(_this,text){
      _this.ctx.fillStyle = "black";
      _this.ctx.fillText(text, getSizeW(.1), getSizeH(.9));


    }
}

export {UserText}