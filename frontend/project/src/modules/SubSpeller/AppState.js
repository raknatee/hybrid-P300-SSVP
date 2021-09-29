import { GridHelper } from "@/modules/renderer/GridHelper.js";
import { SubSpeller } from "@/modules/SubSpeller/SubSpeller.js";
import { style } from "@/modules/renderer/Style.js";
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing.js";


const State = {
    ZERO: 0,
    FlashingP300: 1,
    Targeting: 2
}

class AppState {
    constructor(vueThis) {
        this.appState = State.ZERO
        this.vueThis = vueThis
        this.subSpellers = this.setUpSubSpellers()
        this.subSpellers.forEach((e) => {
            e.setState(this)
        })

        this.msgExperiment = null

    }
    setUpSubSpellers() {
        this.vueThis.ctx.font = `${style.fontSize}px Arial`;

        this.vueThis.ctx.fillStyle = "black";

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
            let coor = gridHelper.getCoordinate(i);
            let thisSubSpller = new SubSpeller(i, coor.x, coor.y)
            subSpellers.push(thisSubSpller);
        }
        return subSpellers
    }
    toZERO() {
        this.appState = State.ZERO

    }
    resetSubSpellersForOfflineMode() {
        this.subSpellers.forEach(subSpeller => {
            subSpeller.reset()
        })
    }
    toFlashingP300() {
        this.subSpellers.forEach((e) => {
            e.createRandomOrder()
        })
        this.appState = State.FlashingP300
    }
    toTarget(indexs, msgExperiment) {
        // indexs => {gridIndex,alpIndex}
        // when the target is showed, msgExperiment is assigned value for ml-server
        this.appState = State.Targeting
        this.indexs = indexs

        let targetSubSpeller = this.findSubSpellerByID(this.indexs.gridIndex)
        targetSubSpeller.setOfflineWatcher(msgExperiment)

    }
    getCurrentState() {
        return this.appState
    }
    getTargetIndex() {
        return this.indexs
    }
    findSubSpellerByID(gridID) {
        return this.subSpellers.find((subSpeller) => subSpeller.gridIndex === gridID)
    }
    findAlphabetByIndex(gridID, index) {
        const subSpeller = this.subSpellers.find((subSpeller) => subSpeller.gridIndex === gridID)
        return subSpeller.alphabets[index]
    }

}

export { AppState, State }