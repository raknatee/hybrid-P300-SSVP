import { subSpellerData, wavesData } from "./info.js"
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing.js"
import { GridHelper } from "@/modules/renderer/GridHelper.js"
import { SinWave } from "@/modules/SinWave.js"
// eslint-disable-next-line no-unused-vars
import { randInt } from "@/modules/Random.js"
import { style } from "@/modules/renderer/Style.js"

class SubSpeller {
    constructor(index, x, y) {
        this.alphabets = subSpellerData[index]

        let waveParam = wavesData[index]
        this.freq = waveParam.freq
        this.phare = waveParam.phare * Math.PI
        this.sinWave = new SinWave(this.freq, this.phare)
        this.x = x
        this.y = y

        this.w = getSizeW(.05)
        this.h = getSizeH(.08)
        this.wMargin = getSizeW(.01)
        this.gridHelper = new GridHelper(this.x, this.y, 3, this.w, this.h, this.wMargin)

    }
    render(_this) {

        let i = 0

        this.alphabets.forEach(element => {

            const coord = this.gridHelper.getCoordinate(i)

            _this.ctx.fillStyle = "black";

            _this.ctx.fillText(element, coord.x, coord.y);
            i++;
        })
    }
    renderFlash(_this) {

        let max = 255
        let min = 0
        let color = this.sinWave.getYNow() * (max - min) + min
        _this.ctx.fillStyle = `rgb(${color},${color},${color})`;
        const coor = this.gridHelper.getCoordinate(randInt(0, this.alphabets.length - 1))
        _this.ctx.fillRect(coor.x - style.fontSize / 4, coor.y - style.fontSize, style.fontSize * 1.2, style.fontSize * 1.3)


        // if (this.sinWave.isUp()) {

        // _this.ctx.fillStyle = "black";
        // const coor = this.gridHelper.getCoordinate(randInt(0, this.alphabets.length - 1))
        // _this.ctx.fillRect(coor.x - style.fontSize / 4, coor.y - style.fontSize, style.fontSize * 1.2, style.fontSize * 1.3)
        // }
    }

}


export { SubSpeller }