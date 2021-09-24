<template lang="">
    <div class="layout">
        <button @click="fullScreen">click me for fullscreen</button>
  
        <canvas id="canvas"></canvas>
    </div>
</template>
<script>
import { setBG } from "@/modules/renderer/BasicSetup.js";
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing.js";

import {getJsonFromWSMessage } from "@/modules/RestAPIHelper/WSHelper.js";
import {getNow} from "@/modules/SinWave.js"

import {AppState} from "@/modules/SubSpeller/AppState.js"
import {sleep} from "@/modules/Time.js"
import { SubSpeller } from "@/modules/SubSpeller/SubSpeller.js";
// import { NextSSVP } from "@/modules/SubSpeller/NextSSVP.js";
import {UserText} from "@/modules/SubSpeller/UserText.js";
import { GridHelper } from "@/modules/renderer/GridHelper.js";

import { style } from "@/modules/renderer/Style.js";

export default {
  data() {
    return {
      canvas: null,
      ctx: null,
      appState: null,
      userText: [],
      ws:null,
      begin_time:null,
      finish_time:null,
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

      this.setUpWS()
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
        let thisSubSpller = new SubSpeller(i, coor.x, coor.y)
        subSpellers.push(thisSubSpller);
      }
      this.appState = new AppState(subSpellers)

      // const nextBtn = new NextSSVP(getSizeW(.55),getSizeH(.9),this.appState)
  


     
      const tick = () => {
        setBG(this);
        UserText.render(this,this.userText.join(','))
        // nextBtn.render(this)
        subSpellers.forEach((subSpeller)=>{
          subSpeller.render(this)
        })


        window.requestAnimationFrame(tick);
      };
      tick();
    },
    setUpWS(){
      this.ws = new WebSocket("ws://localhost:8000/begin_online_mode")
      this.ws.onmessage = async (msg) =>{
          msg = getJsonFromWSMessage(msg)
          if(msg['cmd'] == "next"){
            await sleep(1000)
            this.begin_time =  getNow()
            this.appState.toFlashingP300()
            await sleep(3000)
            this.appState.toZERO()
            this.ws.send(JSON.stringify({
              'begin_time':this.begin_time
            }))
          }
          if(msg['cmd']=="output_model"){
            let alp = this.appState.findAlphabetByIndex(msg["guessed_grid"],msg["guessed_index"])
            this.userText.push(alp)
       
          }
      }
    }
  },
};
</script>
<style lang="scss" scoped>
</style>