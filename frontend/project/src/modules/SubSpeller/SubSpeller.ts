import { subSpellerData, wavesData } from "./info"
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing"
import { GridHelper } from "@/modules/renderer/GridHelper"
import { SinWave, getNow } from "@/modules/SinWave"
import {  checkerboard } from "@/modules/Random"
import { style } from "@/modules/renderer/Style"
import { AppState,State } from "./AppState"


class SubSpeller {
    gridIndex:number
    alphabets:string[]
    freq:number
    phare:number
    sinWave:SinWave
    x:number
    y:number
    w:number
    h:number

    wMargin:number
    gridHelper:GridHelper
    state:AppState|undefined

    startTime:number|undefined
    spawnTime:number
    ttl:number

    currentIndexes:CurrentIndex[]
    randomIndex:number[]

    do_need_to_watch_the_target:boolean
    msgExperiment:any
    constructor(index:number, x:number, y:number, spawnTime:number, ttl:number) {
        this.gridIndex = index
        this.alphabets = subSpellerData[this.gridIndex]!

        const waveParam = wavesData[this.gridIndex]!
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
      
        this.currentIndexes = []
        this.spawnTime = spawnTime // ms
        this.ttl = ttl // ms

        // P300
        this.randomIndex = []

        // For Offline mode creates a message
        this.do_need_to_watch_the_target = false



    }
    setState(appState:AppState):void {
        this.state = appState
    }
    render(ctx:CanvasRenderingContext2D):void {

       
        this.renderFlash(ctx)
        this.renderTarget(ctx)

        let i = 0
        this.alphabets.forEach(element => {

            const coord = this.gridHelper.getCoordinate(i)

           ctx.fillStyle = "black";

           ctx.fillText(element, coord.x, coord.y);
            i++;
        })
    }
    setStartForP300():void {
        // TODO : if we want to have a overlap array, I need to make sure that. 
        // Do not have two alphabets which are close togerther SHOW at the same time

        this.randomIndex = checkerboard(this.alphabets.length)

        this.startTime = getNow()
        for (let i = 0; i < this.randomIndex.length; i++) {

            setTimeout(() => {
                this._pushToCurrentIndex(i)

            }, this.spawnTime * i)




        }

    }
    _pushToCurrentIndex(i:number):void {

        this.currentIndexes.push(
            new CurrentIndex(this.randomIndex[i],getNow())
        )

        if (this.do_need_to_watch_the_target) {
            const targetIndex = this.state!.getTargetIndex()
            let is_activated = false
            if (targetIndex!.alpIndex === this.randomIndex[i]) {
                is_activated = true
            } else {
                is_activated = false
            }
            const timeForStamp = getNow()
            if (is_activated) {
                console.log(timeForStamp, targetIndex!.alpIndex, this.randomIndex[i])
            }
            this.msgExperiment.data.push({
                "timestamp": timeForStamp,
                "is_target_activated": is_activated
            })
        }
    }
    renderFlash(ctx:CanvasRenderingContext2D):void {
      
        if (this.state!.getCurrentState() != State.FlashingP300) {
            return
        }
        if (this.currentIndexes.length <= 0) {
            return
        }

        const now = getNow()


        if (now - this.currentIndexes[0].time >= this.ttl / 1000) {
            this.currentIndexes.shift()
        }





        const max = 255
        const min = 0
        const color = this.sinWave.getYNow() * (max - min) + min
        ctx.fillStyle = `rgb(${color},${color},${color})`;

        this.currentIndexes.forEach((e) => {
            const coor = this.gridHelper.getCoordinate(e.index)
            ctx.fillRect(coor.x - style.fontSize / 4, coor.y - style.fontSize, style.fontSize * 1.2, style.fontSize * 1.3)
        })







    }
    renderTarget(ctx:CanvasRenderingContext2D):void {
       
        if (this.state!.getCurrentState() != State.Targeting) {
            return
        }
        const targetIndexs = this.state!.getTargetIndex()
        if (targetIndexs!.gridIndex != this.gridIndex) {
            return
        }

      ctx.fillStyle = "red"
        const coor = this.gridHelper.getCoordinate(targetIndexs!.alpIndex)
      ctx.fillRect(coor.x - style.fontSize / 4, coor.y - style.fontSize, style.fontSize * 1.2, style.fontSize * 1.3)

    }
    setOfflineWatcher(msgExperiment:any):void {
        this.do_need_to_watch_the_target = true
        this.msgExperiment = msgExperiment
    }
    reset():void{
        this.do_need_to_watch_the_target = false
    }
}
class CurrentIndex{
    index:number
    time:number
    constructor(index:number,time:number){
        this.index=index
        this.time=time
    }
}


export { SubSpeller, State }