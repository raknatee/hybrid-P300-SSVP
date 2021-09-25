import { subSpellerData, wavesData } from "./info.js"
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing.js"
import { GridHelper } from "@/modules/renderer/GridHelper.js"
import { SinWave, getNow } from "@/modules/SinWave.js"
// eslint-disable-next-line no-unused-vars
import { randInt, rangeRandomArray } from "@/modules/Random.js"
import { style } from "@/modules/renderer/Style.js"
import { State } from "./AppState.js"

class SubSpeller {
    constructor(index, x, y) {
        this.gridIndex = index
        this.alphabets = subSpellerData[this.gridIndex]

        let waveParam = wavesData[this.gridIndex]
        this.freq = waveParam.freq
        this.phare = waveParam.phare * Math.PI
        this.sinWave = new SinWave(this.freq, this.phare)
        this.x = x
        this.y = y

        this.w = getSizeW(.05)
        this.h = getSizeH(.08)
        this.wMargin = getSizeW(.01)
        this.gridHelper = new GridHelper(this.x, this.y, 3, this.w, this.h, this.wMargin)

        // timing
        this.previousTime = null
        this.currentIndex = 0
        this.state = null

        // P300
        this.randomIndex = []

        // For Offline mode
        this.do_need_watch = false
        this.last_index_which_insert_to_msg_experiment = -1


    }
    setState(appState) {
        this.state = appState
    }
    render(_this) {

        this.renderFlash(_this)
        this.renderTarget(_this)

        let i = 0
        this.alphabets.forEach(element => {

            const coord = this.gridHelper.getCoordinate(i)

            _this.ctx.fillStyle = "black";

            _this.ctx.fillText(element, coord.x, coord.y);
            i++;
        })
    }
    createRandomOrder() {
        this.randomIndex = rangeRandomArray(this.alphabets.length)
    }
    renderFlash(_this) {
        if (this.state.getCurrentState() != State.FlashingP300 && this.randomIndex.length > 0) {
            return
        }
        let now = getNow()

        if (this.previousTime === null || now - this.previousTime >= .2) {
            this.previousTime = now
            this.currentIndex = this.randomIndex.pop()
        }


        let max = 255
        let min = 0
        let color = this.sinWave.getYNow() * (max - min) + min
        _this.ctx.fillStyle = `rgb(${color},${color},${color})`;
        const coor = this.gridHelper.getCoordinate(this.currentIndex)
        _this.ctx.fillRect(coor.x - style.fontSize / 4, coor.y - style.fontSize, style.fontSize * 1.2, style.fontSize * 1.3)

        if (!this.do_need_watch) {
            return
        }
        if (this.currentIndex == undefined) {
            return
        }
        if (this.currentIndex == this.last_index_which_insert_to_msg_experiment) {
            return
        }
        this.last_index_which_insert_to_msg_experiment = this.currentIndex

        let targetIndex = this.state.getTargetIndex()
        let is_activated = false
        if (targetIndex.alpIndex === this.currentIndex) {
            is_activated = true
        } else {
            is_activated = false
        }
        let timeForStamp = getNow()
        if (is_activated) {
            console.log(timeForStamp, is_activated)
        }
        this.msgExperiment.data.push({
            "timestamp": timeForStamp,
            "is_target_activated": is_activated
        })


    }
    renderTarget(_this) {
        if (this.state.getCurrentState() != State.Targeting) {
            return
        }
        let targetIndexs = this.state.getTargetIndex()
        if (targetIndexs.gridIndex != this.gridIndex) {
            return
        }

        _this.ctx.fillStyle = "red"
        const coor = this.gridHelper.getCoordinate(targetIndexs.alpIndex)
        _this.ctx.fillRect(coor.x - style.fontSize / 4, coor.y - style.fontSize, style.fontSize * 1.2, style.fontSize * 1.3)

    }
    setOfflineWatcher(msgExperiment) {
        this.do_need_watch = true
        this.msgExperiment = msgExperiment
    }
    reset() {
        this.do_need_watch = false
    }
}


export { SubSpeller, State }