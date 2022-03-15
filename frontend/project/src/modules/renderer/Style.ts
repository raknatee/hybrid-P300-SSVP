// eslint-disable-next-line no-unused-vars
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing"

type Style = {
    fontSize:number
    boxHighlightWScale:number
    boxHighlightHScale:number
}
const style:Style = {
    fontSize: getSizeW(0.04),
    boxHighlightWScale:1.3,
    boxHighlightHScale:1.3
    // boxHighlightWScale:1.2*4,
    // boxHighlightHScale:1.3*4
}
export {
    style
}