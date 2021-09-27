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
// import { NextSSVP } from "@/modules/SubSpeller/NextSSVP.js";
import {UserText} from "@/modules/SubSpeller/UserText.js";
import {choise} from "@/modules/Random.js"

export default {
  data() {
    return {
      canvas: null,
      ctx: null,
      appState: null,
      userText: [],
      ws:null,
      begin_time:null,
  
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
    
      if(this.$route.params.mode === "online"){
        this.setUpWSOnline()
      }
       if(this.$route.params.mode === "offline"){
        this.setUpWSOffline()
      }
      this.canvas.width = getSizeW(1);
      this.canvas.height = getSizeH(1);

      
      this.appState = new AppState(this)

      // const nextBtn = new NextSSVP(getSizeW(.55),getSizeH(.9),this.appState)
  


     
      const tick = () => {
        setBG(this);
        UserText.render(this,this.userText.join(','))
        // nextBtn.render(this)
        this.appState.subSpellers.forEach((subSpeller)=>{
          subSpeller.render(this)
        })


        window.requestAnimationFrame(tick);
      };
      tick();
    },
    setUpWSOnline(){
      this.ws = new WebSocket(`ws://${location.hostname}:8000/begin_online_mode`)
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
    },
    setUpWSOffline(){
      this.ws = new WebSocket(`ws://${location.hostname}:8000/begin_offline_mode`)
      this.ws.onmessage = async (msg) =>{
        msg = getJsonFromWSMessage(msg)

        if(msg["cmd"]== "next"){


          // let target = {'gridIndex':2,'alpIndex':2}
          // let target = {'gridIndex':10,'alpIndex':2}
          // let target = {'gridIndex':11,'alpIndex':2}
          let target = choise([
            {'gridIndex':2,'alpIndex':2},
            {'gridIndex':10,'alpIndex':2},
            {'gridIndex':11,'alpIndex':2},
          ])
          let msgExperiment = {
            "target_grid": target.gridIndex,
            "terget_index": target.alpIndex,
            "data":[]
          }
          await sleep(1000)
          this.appState.toTarget(target,msgExperiment)
          await sleep(1000)
          this.appState.toZERO()
          await sleep(1000)
          this.appState.toFlashingP300()
          await sleep(3000)
          this.appState.toZERO()
          this.appState.resetSubSpellersForOfflineMode()
          console.log(msgExperiment)
          this.ws.send(JSON.stringify(msgExperiment))
        }
      }
    }
  },
};
</script>
<style lang="scss" scoped>
</style>