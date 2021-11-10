import { getSizeW, getSizeH } from "@/modules/renderer/Sizing";

class FPSText {
    static render(ctx:CanvasRenderingContext2D, text:string):void {
       
     ctx.fillStyle = "#4287f5";
     ctx.fillText(text, getSizeW(.05), getSizeH(.95));



    } 
}

export { FPSText }