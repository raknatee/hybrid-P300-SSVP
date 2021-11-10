import { getSizeW, getSizeH } from "@/modules/renderer/Sizing";
import { style } from "../renderer/Style";

class FPSText {
    static render(ctx:CanvasRenderingContext2D, text:string):void {
       
     ctx.font = `${style.fontSize/2}px Arial`;
     ctx.fillStyle = "#4287f5";


     if(text!="60"){
         text += " => your FPS isnt 60HZ, SSVEP frequency might not be working"
     }
     ctx.fillText(text, getSizeW(.05), getSizeH(.95));
     ctx.font = `${style.fontSize}px Arial`;
    


    } 
}

export { FPSText }