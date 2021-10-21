
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
export {HYPSCommands,DBConfig,SleepDetails,TargetDetails,CommandType}