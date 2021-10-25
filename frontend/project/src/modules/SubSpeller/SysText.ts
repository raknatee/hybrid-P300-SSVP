import { getSizeW, getSizeH } from "@/modules/renderer/Sizing";


class SysText {
    static render(ctx:CanvasRenderingContext2D, text:string):void {
       
     ctx.fillStyle = "red";
     ctx.fillText(text, getSizeW(.4), getSizeH(.75));


    }
}

export { SysText }