<template lang="">
    <div class="layout">
        <button @click="fullScreen">click me for fullscreen</button>
        <canvas id="canvas"></canvas>
    </div>
</template>
<script>
import { setBG } from "@/modules/renderer/BasicSetup.js";
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing.js";

import {AppState} from "@/modules/SubSpeller/AppState.js"
import {sleep} from "@/modules/Time.js"
import { SubSpeller } from "@/modules/SubSpeller/SubSpeller.js";
import { NextSSVP } from "@/modules/SubSpeller/NextSSVP.js";
import {UserText} from "@/modules/SubSpeller/UserText.js";
import { GridHelper } from "@/modules/renderer/GridHelper.js";

import { style } from "@/modules/renderer/Style.js";

export default {
  data() {
    return {
      canvas: null,
      ctx: null,
      appState: new AppState(),
      userText: "dummy text"
    };
  },
  mounted() {
    this.canvas = document.getElementById("canvas");
    this.ctx = this.canvas.getContext("2d");
  },
  methods: {
    fullScreen() {
      this.canvas.requestFullscreen();
      setTimeout(() => {
        this.run();
      }, 500);
    },

    run() {
      this.canvas.width = getSizeW(1);
      this.canvas.height = getSizeH(1);

      this.ctx.font = `${style.fontSize}px Arial`;

      this.ctx.fillStyle = "black";

      const gridHelper = new GridHelper(
        getSizeW(0.05),
        getSizeH(0.08),
        4,
        getSizeW(0.25),
        getSizeH(0.3)
      );
      const subSpellers = [];
      for (let i = 0; i < 12; i++) {
        if (i == 8 || i == 9) {
          continue;
        }
        let coor = gridHelper.getCoordinate(i);
        let thisSubSpller = new SubSpeller(i, coor.x, coor.y,this.appState)
        subSpellers.push(thisSubSpller);
      }

      const nextBtn = new NextSSVP(getSizeW(.55),getSizeH(.9),this.appState)
  
      setInterval( async ()=>{
        this.appState.toTarget({gridIndex:4,alpIndex:5})
        await sleep(2000)
        this.appState.toFlashingP300()
        await sleep(2000)
        this.appState.toZERO()
      },5000)

     
      const tick = () => {
        setBG(this);
        UserText.render(this,this.userText)
        nextBtn.render(this)
        subSpellers.forEach((subSpeller)=>{
          subSpeller.render(this)
        })


        window.requestAnimationFrame(tick);
      };
      tick();
    },
  },
};
</script>
<style lang="scss" scoped>
</style>