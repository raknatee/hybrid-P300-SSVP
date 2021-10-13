import { style } from "@/modules/renderer/Style"
import { SinWave } from "@/modules/SinWave"
import { State } from "./SubSpeller.js"
import {AppState} from "@/modules/SubSpeller/AppState"
class NextSSVP {
    x:number
    y:number
    sinWave:SinWave
    state:AppState
    constructor(x:number, y:number, appState:AppState) {
        this.x = x
        this.y = y
        this.sinWave = new SinWave(14.4, 1.5 * Math.PI)
        this.state = appState

    }
    render(_this:any) {
        this.renderFlash(_this)

        _this.ctx.fillStyle = "black";
        _this.ctx.fillText("NEXT", this.x, this.y);
    }
    renderFlash(_this:any) {
        if (this.state.getCurrentState() != State.ZERO) {
            return
        }
        const max = 255
        const min = 0
        const color = this.sinWave.getYNow() * (max - min) + min
        _this.ctx.fillStyle = `rgb(${color},${color},${color})`;

        _this.ctx.fillRect(this.x - style.fontSize / 4, this.y - style.fontSize, style.fontSize * 4.2, style.fontSize * 1.3)

        // if (this.sinWave.isUp()) {
        //     _this.ctx.fillStyle = "black";
        //     _this.ctx.fillRect(this.x - style.fontSize / 4, this.y - style.fontSize, style.fontSize * 4.2, style.fontSize * 1.3)

        // }

    }
}

export { NextSSVP }