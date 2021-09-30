import { subSpellerData, wavesData } from "./info.js"
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing.js"
import { GridHelper } from "@/modules/renderer/GridHelper.js"
import { SinWave, getNow } from "@/modules/SinWave.js"
// eslint-disable-next-line no-unused-vars
import { randInt, rangeRandomArray } from "@/modules/Random.js"
import { style } from "@/modules/renderer/Style.js"
import { State } from "./AppState.js"


class SubSpeller {
    constructor(index, x, y, spawnTime, ttl) {
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
        this.state = null


        // timing
        this.startTime = null
        this.currentIndexes = []
        this.spawnTime = spawnTime // ms
        this.ttl = ttl // ms

        // P300
        this.randomIndex = []

        // For Offline mode creates a message
        this.do_need_to_watch_the_target = false



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
    setStartForP300() {
        // TODO : if we want to have a overlap array, I need to make sure that. 
        // Do not have two alphabets which are close togerther SHOW at the same time

        this.randomIndex = rangeRandomArray(this.alphabets.length)
        console.log(this.randomIndex)
        this.startTime = getNow()
        for (let i = 0; i < this.randomIndex.length; i++) {

            setTimeout(() => {
                this._pushToCurrentIndex(i)

            }, this.spawnTime * i)




        }

    }
    _pushToCurrentIndex(i) {

        this.currentIndexes.push({
            'index': this.randomIndex[i],
            'time': getNow()
        })

        if (this.do_need_to_watch_the_target) {
            let targetIndex = this.state.getTargetIndex()
            let is_activated = false
            if (targetIndex.alpIndex === this.randomIndex[i]) {
                is_activated = true
            } else {
                is_activated = false
            }
            let timeForStamp = getNow()
            if (is_activated) {
                console.log(timeForStamp, targetIndex.alpIndex, this.randomIndex[i])
            }
            this.msgExperiment.data.push({
                "timestamp": timeForStamp,
                "is_target_activated": is_activated
            })
        }
    }
    renderFlash(_this) {
        if (this.state.getCurrentState() != State.FlashingP300) {
            return
        }
        if (this.currentIndexes.length <= 0) {
            return
        }

        let now = getNow()


        if (now - this.currentIndexes[0].time >= this.ttl / 1000) {
            this.currentIndexes.shift()
        }





        let max = 255
        let min = 0
        let color = this.sinWave.getYNow() * (max - min) + min
        _this.ctx.fillStyle = `rgb(${color},${color},${color})`;

        this.currentIndexes.forEach((e) => {
            const coor = this.gridHelper.getCoordinate(e.index)
            _this.ctx.fillRect(coor.x - style.fontSize / 4, coor.y - style.fontSize, style.fontSize * 1.2, style.fontSize * 1.3)
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
        this.do_need_to_watch_the_target = true
        this.msgExperiment = msgExperiment
    }
    reset() {
        this.do_need_to_watch_the_target = false
    }
}


export { SubSpeller, State }