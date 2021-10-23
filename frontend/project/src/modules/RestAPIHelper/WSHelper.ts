enum CMDType{
    next="next",
    output_model="output_model"
}

class RoundCMD{
    cmd:CMDType
    guessed_grid:number|undefined
    guessed_index_order:number|undefined


    constructor(cmd:CMDType,guessed_grid?:number,guessed_index_order?:number){
     
        this.cmd= cmd
        this.guessed_grid=guessed_grid
        this.guessed_index_order = guessed_index_order
    }
   
}
const getJsonFromWSMessage = (msg:MessageEvent<any>):RoundCMD => {
    return JSON.parse(msg.data)
}

export { getJsonFromWSMessage,RoundCMD }