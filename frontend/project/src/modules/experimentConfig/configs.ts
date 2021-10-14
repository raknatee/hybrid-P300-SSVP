import {choise,randInt} from "@/modules/Random"
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

const experimentConfigDefault:any = {
    
        "cmds": [
            {
                "cmd": "sleep",
                "details": {
                    "time": 10000
                },
                "repeat": 1
            },
            {
                "cmd": "target",
                "details": {
                    "gridIndex": 6,
                    "alpIndex": 5
                },
                "repeat": 5
            },
            {
                "cmd": "target",
                "details": {
                    "gridIndex": 0,
                    "alpIndex": 4
                },
                "repeat": 5
            },
            {
                "cmd": "target",
                "details": {
                    "gridIndex": 10,
                    "alpIndex": 4
                },
                "repeat": 5
            },
            {
                "cmd": "target",
                "details": {
                    "gridIndex": 10,
                    "alpIndex": 0
                },
                "repeat": 5
            },
            {
                "cmd": "target",
                "details": {
                    "gridIndex": 11,
                    "alpIndex": 8
                },
                "repeat": 5
            },
            {
                "cmd": "sleep",
                "details": {
                    "time": 5000
                },
                "repeat": 1
            },
            {
                "cmd": "target",
                "details": {
                    "gridIndex": 0,
                    "alpIndex": 5
                },
                "repeat": 5
            },
            {
                "cmd": "target",
                "details": {
                    "gridIndex": 1,
                    "alpIndex": 0
                },
                "repeat": 5
            },
            {
                "cmd": "target",
                "details": {
                    "gridIndex": 4,
                    "alpIndex": 6
                },
                "repeat": 5
            },
            {
                "cmd": "target",
                "details": {
                    "gridIndex": 0,
                    "alpIndex": 0
                },
                "repeat": 5
            },
            {
                "cmd": "target",
                "details": {
                    "gridIndex": 7,
                    "alpIndex": 8
                },
                "repeat": 5
            }
        ],
        "repeat": 6
    
}
// for(let i=0;i<10;i++){
//     experimentConfigDefault.cmds.push(
//         {
//             "cmd": "target",
//             "details": { "gridIndex": choise([0,1,2,3,4,5,6,7,10,11]), "alpIndex": randInt(0,8) },
//             "repeat": 5
//         }
    
//     )
// }

export { experimentConfigDefault,OfflineCommand }