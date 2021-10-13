import { style } from "@/modules/renderer/Style.js"
import { SinWave } from "@/modules/SinWave.js"
import {State} from "./SubSpeller.js"
class NextSSVP {
    constructor(x, y,appState) {
        this.x = x
        this.y = y
        this.sinWave = new SinWave(14.4, 1.5 * Math.PI)
        this.state = appState

    }
    render(_this) {
        this.renderFlash(_this)

        _this.ctx.fillStyle = "black";
        _this.ctx.fillText("NEXT", this.x, this.y);
    }
    renderFlash(_this) {
        if(this.state.getCurrentState()!=State.ZERO){
            return
        }
        let max = 255
        let min = 0
        let color = this.sinWave.getYNow() * (max - min) + min
        _this.ctx.fillStyle = `rgb(${color},${color},${color})`;

        _this.ctx.fillRect(this.x - style.fontSize / 4, this.y - style.fontSize, style.fontSize * 4.2, style.fontSize * 1.3)

        // if (this.sinWave.isUp()) {
        //     _this.ctx.fillStyle = "black";
        //     _this.ctx.fillRect(this.x - style.fontSize / 4, this.y - style.fontSize, style.fontSize * 4.2, style.fontSize * 1.3)

        // }

    }
}

export { NextSSVP }