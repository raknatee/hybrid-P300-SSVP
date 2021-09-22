const State ={
    ZERO:0,
    FlashingP300:1,
    Targeting:2
}

class AppState{
    constructor(){
        this.appState = State.ZERO
     
    }
    toZERO(){
        this.appState = State.ZERO
    }
    toFlashingP300(){
        this.appState = State.FlashingP300
    }
    toTarget(indexs){
        // indexs => {gridIndex,alpIndex}
        this.appState = State.Targeting
        this.indexs = indexs
        
    }
    getCurrentState(){
        return this.appState
    }
    getTargetIndex(){
        return this.indexs
    }

}

export {AppState, State}