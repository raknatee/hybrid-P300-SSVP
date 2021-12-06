import {getPerformanceNow} from "@/modules/Time"
class FPS{

    static lastTick:number
    static tick():void{
        FPS.lastTick=getPerformanceNow()
    }
    static get():number{
        const now = getPerformanceNow()
        if(FPS.lastTick==undefined){
            return 0
        }
        const fps = Math.round(1/(now-FPS.lastTick))
    
            return fps
        
    }
}

export {FPS}