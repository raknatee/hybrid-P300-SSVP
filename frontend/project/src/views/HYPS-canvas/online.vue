<template lang="">
    <div class="layout">
        <button @click="fullScreen">click me for fullscreen</button>
        <canvas id="canvas"></canvas>
    </div>
</template>
<script>
// eslint-disable-next-line no-unused-vars
import { SinWave, getNow } from "@/modules/SinWave.js";
// eslint-disable-next-line no-unused-vars
import {setBG} from "@/modules/renderer/BasicSetup.js"
import {getSizeW,getSizeH} from "@/modules/renderer/Sizing.js"
import {SubSpeller} from "@/modules/SubSpeller/SubSpeller.js"
import { GridHelper } from "@/modules/renderer/GridHelper.js"
import { style } from "@/modules/renderer/Style.js"

export default {
  data() {
    return {
      canvas: null,
      ctx: null,
    };
  },
  mounted() {

    this.canvas = document.getElementById("canvas");
    this.ctx = this.canvas.getContext("2d");
    

  },
  methods: {
    fullScreen(){
        this.canvas.requestFullscreen()
        setTimeout(()=>{
            this.run()
        },500)
    },

    run() {
    //   let thisWave = new SinWave(16, 0);
      this.canvas.width = getSizeW(1)
      this.canvas.height = getSizeH(1);
   
      setBG(this)
      this.ctx.font = `${style.fontSize}px Arial`;
    
      this.ctx.fillStyle = "black";

    const gridHelper = new GridHelper(getSizeW(.05),getSizeH(.08),4,getSizeW(.25),getSizeH(.3))
    const subSpellers = []
    for(let i=0;i<12;i++){
        if(i== 8 || i==9){
            subSpellers.push(null)
            continue
        }
        let coor = gridHelper.getCoordinate(i)
        subSpellers.push(new SubSpeller(i,coor.x,coor.y))

    }
      

      const tick = () => {
     
          for(let i=0;i<12;i++){
              let subSpeller = subSpellers[i]
              if(subSpeller === null){
                  continue
              }
          
              subSpeller.render(this)
              subSpeller.renderFlash(this)
          }
         
    
        window.requestAnimationFrame(tick);
      };
      tick();
    },
  },
};
</script>
<style lang="scss" scoped>
// .layout {
//   display: flex;
//   flex-direction: column;
// }
</style>