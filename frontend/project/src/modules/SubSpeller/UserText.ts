import { getSizeW, getSizeH } from "@/modules/renderer/Sizing";


class UserText {
    static render(ctx:CanvasRenderingContext2D, text:string):void {
       
      ctx.fillStyle = "black";
       ctx.fillText(text, getSizeW(.1), getSizeH(.9));


    }
}

export { UserText }