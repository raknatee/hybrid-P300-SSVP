import { getSizeW, getSizeH } from "@/modules/renderer/Sizing";


class UserText {
    static render(vueThis:any, text:string) {
       
        vueThis.ctx.fillStyle = "black";
        vueThis.ctx.fillText(text, getSizeW(.1), getSizeH(.9));


    }
}

export { UserText }