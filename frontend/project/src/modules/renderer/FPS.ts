import {getPerformanceNow} from "@/modules/Time"
class FPS{

    static lastTick:number
    static countFrame:number
    static lastFPS:number
    static init():void{
        FPS.lastTick=-1
        FPS.countFrame = 0
        FPS.lastFPS = -1
    }
    static tick():void{
       if(FPS.lastTick == -1){
           FPS.lastTick=getPerformanceNow()
       }
        FPS.countFrame += 1
        
    }
    static get():number{
        const now = getPerformanceNow()
      
        const timeInterval = 1
      
 
        if(now - FPS.lastTick >=timeInterval){
            FPS.lastFPS = FPS.countFrame/timeInterval
            FPS.lastTick = -1
            FPS.countFrame = 0
        }
        
    
        return FPS.lastFPS
        
    }
}

export {FPS}