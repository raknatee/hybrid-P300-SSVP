
enum CommandType{
    target="target" ,
    sleep = "sleep"
}
type HYPSCommands = {
    cmds: HYPSCommand[],
    repeat:number
}
type HYPSCommand = {
    "cmd":CommandType
    "details": SleepDetails|TargetDetails
    repeat:number

}

type SleepDetails = {
    "time":number
}
type TargetDetails = {
    "gridIndex":number
    "alpIndex":number
}

type DBConfig = {
    "current_participant_id":string
}

type P300Config = {
    "spawn":number
    "ttl":number
    "time_per_round":number
}
export {HYPSCommands,DBConfig,SleepDetails,TargetDetails,CommandType,P300Config}