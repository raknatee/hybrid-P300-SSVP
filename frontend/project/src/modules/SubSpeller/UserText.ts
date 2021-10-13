import { getSizeW, getSizeH } from "@/modules/renderer/Sizing";


class UserText {
    static render(_this:any, text:string) {
       
        _this.ctx.fillStyle = "black";
        _this.ctx.fillText(text, getSizeW(.1), getSizeH(.9));


    }
}

export { UserText }