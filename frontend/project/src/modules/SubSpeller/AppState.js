const State = {
    ZERO: 0,
    FlashingP300: 1,
    Targeting: 2
}

class AppState {
    constructor(subSpellers) {
        this.appState = State.ZERO
        this.subSpellers = subSpellers
        this.subSpellers.forEach((e) => {
            e.setState(this)
        })

    }
    toZERO() {
        this.appState = State.ZERO
    }
    toFlashingP300() {
        this.subSpellers.forEach((e) => {
            e.createRandomOrder()
        })
        this.appState = State.FlashingP300
    }
    toTarget(indexs) {
        // indexs => {gridIndex,alpIndex}
        this.appState = State.Targeting
        this.indexs = indexs

    }
    getCurrentState() {
        return this.appState
    }
    getTargetIndex() {
        return this.indexs
    }
    findAlphabetByIndex(gridID, index) {
        const subSpeller = this.subSpellers.find((subSpeller) => subSpeller.gridIndex === gridID)
        return subSpeller.alphabets[index]
    }

}

export { AppState, State }