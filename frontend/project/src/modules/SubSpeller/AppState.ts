import { GridHelper } from "@/modules/renderer/GridHelper";
import { SubSpeller } from "@/modules/SubSpeller/SubSpeller";
import { style } from "@/modules/renderer/Style";
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing";

enum State{
    ZERO,
    FlashingP300,
    Targeting
}

class TargetIndex{
    gridIndex:number
    alpIndex:number
    constructor(gridIndex:number,alpIndex:number){
        this.gridIndex=gridIndex
        this.alpIndex=alpIndex
    }
}
class AppState {
    appState:State
    canvas:HTMLCanvasElement
    ctx:CanvasRenderingContext2D
    subSpellers:SubSpeller[]
    msgExperiment:any
    targetIndex:TargetIndex|undefined
    constructor(canvas:HTMLCanvasElement,ctx:CanvasRenderingContext2D, spawn:number, ttl:number) {
      
        this.appState = State.ZERO
        this.canvas=canvas
        this.ctx=ctx
        this.subSpellers = this.setUpSubSpellers(spawn, ttl)
        this.subSpellers.forEach((e) => {
            e.setState(this)
        })

        this.msgExperiment = null

    }
    setUpSubSpellers(spawn:number, ttl:number):SubSpeller[] {
        this.ctx.font = `${style.fontSize}px Arial`;

        this.ctx.fillStyle = "black";

        const gridHelper = new GridHelper(
            getSizeW(0.05),
            getSizeH(0.08),
            4,
            getSizeW(0.25),
            getSizeH(0.3)
        );
        const subSpellers = [];
        for (let i = 0; i < 12; i++) {
            if (i == 8 || i == 9) {
                continue;
            }
            const coor = gridHelper.getCoordinate(i);
            const thisSubSpller = new SubSpeller(i, coor.x, coor.y, spawn, ttl)
            subSpellers.push(thisSubSpller);
        }
        return subSpellers
    }
    toZERO():void {
        this.appState = State.ZERO

    }
    doneRound():void {
        this.subSpellers.forEach(subSpeller => {
            subSpeller.reset()
        })
    }
    toFlashingP300():void {
        this.subSpellers.forEach((e) => {
            e.setStartForP300()
        })

        this.appState = State.FlashingP300


    }
    toTarget(targetIndex:TargetIndex, msgExperiment:any):void {
        // indexs => {gridIndex,alpIndex}
        // when the target is showed, msgExperiment is assigned value for ml-server
        this.appState = State.Targeting
        this.targetIndex = targetIndex

        const targetSubSpeller = this.findSubSpellerByID(this.targetIndex.gridIndex)!
        targetSubSpeller.setOfflineWatcher(msgExperiment)

    }
    getCurrentState():State {
        return this.appState
    }
    getTargetIndex():TargetIndex|undefined {
        return this.targetIndex
    }
    findSubSpellerByID(gridID:number):SubSpeller|undefined {
        return this.subSpellers.find((subSpeller) => subSpeller.gridIndex === gridID)
    }
    findAlphabetByIndexOrder(gridID:number, index:number):string {
        const subSpeller = this.subSpellers.find((subSpeller) => subSpeller.gridIndex === gridID)
        const i =  subSpeller!.randomIndex[index]
        return subSpeller!.alphabets[i]
    }

}

export { AppState, State }