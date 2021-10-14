import { getSizeW, getSizeH } from "@/modules/renderer/Sizing";


class SysText {
    static render(vueThis:any, text:string) {
       
        vueThis.ctx.fillStyle = "red";
        vueThis.ctx.fillText(text, getSizeW(.4), getSizeH(.75));


    }
}

export { SysText }