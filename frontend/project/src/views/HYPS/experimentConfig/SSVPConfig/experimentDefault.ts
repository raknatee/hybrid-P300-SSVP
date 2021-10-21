import { CommandType, HYPSCommands } from "../ConfigType";

const ssvpConfig:HYPSCommands = {
    cmds:[
        {cmd:CommandType.sleep,details:{time:5000},repeat:1},
        {cmd:CommandType.target,details:{gridIndex:0,alpIndex:4},repeat:1},
        {cmd:CommandType.target,details:{gridIndex:1,alpIndex:4},repeat:1},
        {cmd:CommandType.target,details:{gridIndex:2,alpIndex:4},repeat:1},
        {cmd:CommandType.target,details:{gridIndex:3,alpIndex:4},repeat:1},

        {cmd:CommandType.target,details:{gridIndex:4,alpIndex:4},repeat:1},
        {cmd:CommandType.target,details:{gridIndex:5,alpIndex:4},repeat:1},
        {cmd:CommandType.target,details:{gridIndex:6,alpIndex:4},repeat:1},
        {cmd:CommandType.target,details:{gridIndex:7,alpIndex:4},repeat:1},

        {cmd:CommandType.target,details:{gridIndex:10,alpIndex:4},repeat:1},
        {cmd:CommandType.target,details:{gridIndex:11,alpIndex:4},repeat:1},
    ],
    repeat:1
}

export {ssvpConfig}