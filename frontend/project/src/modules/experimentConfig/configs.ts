enum CommandType{
    target="target" ,
    sleep = "sleep"
}
class OfflineCommand{
    cmd:CommandType
    details:any
    constructor(cmd:string,details:any){
        switch(cmd){
            case CommandType.target:
                this.cmd = CommandType.target
                break
            case CommandType.sleep:
                this.cmd = CommandType.sleep
                break

            default:
                throw new Error("CommandType not found")
                
        }
      
       
        this.details = details
    }
}


const experimentConfigDefault = {
    "cmds": [{
            "cmd": "target",
            "details": { "gridIndex": 2, "alpIndex": 2 },
            "repeat": 1
        },
        {
            "cmd": "sleep",
            "details": { "time": 10000 },
            "repeat": 1
        },
        {
            "cmd": "target",
            "details": { "gridIndex": 10, "alpIndex": 1 },
            "repeat": 1
        },
        {
            "cmd": "sleep",
            "details": { "time": 10000 },
            "repeat": 1
        },
        {
            "cmd": "target",
            "details": { "gridIndex": 11, "alpIndex": 8 },
            "repeat": 1
        },
        {
            "cmd": "sleep",
            "details": { "time": 10000 },
            "repeat": 1
        }
    ],
    "repeat": 2
}
export { experimentConfigDefault,OfflineCommand }