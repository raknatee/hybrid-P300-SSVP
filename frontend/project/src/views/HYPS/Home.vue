<template lang="">
    <div class="layout">
        <h1>Step 1</h1>
        <h1>Database Config</h1>
        <p>please set this and do submit first before going to next step</p>

        <textarea v-model="DBConfig" rows="7" cols="50"></textarea>
        <button @click="submitDBConfig">submit</button>
        <p>{{DBConfigStatus}}</p>

        <hr>
        <h1>Step 2</h1>
        <h1>P300 Config</h1>
        <textarea v-model="P300Config" rows="7" cols="50"></textarea>
        <br>

        <div v-if="mode=='offline'">
        <h1  >Experiment Config</h1>
        <textarea v-model="ExperimentConfigOffline" rows="20" cols="50"></textarea>

        </div>
      
        <p>Before running the experiment please set your EEG headset and run EEG-client. You can check that is it okay or not by click DBViewer </p>
        <router-link to="/dbview"  target="_blank">Click me for DBViewer </router-link>
        <br>
        <button @click="fullScreen">click me for fullscreen and run the experiment</button>
        
        <canvas id="canvas"></canvas>
    </div>
</template>
<script lang="ts">
import { setBG } from "@/modules/renderer/BasicSetup";
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing";

import { getJsonFromWSMessage } from "@/modules/RestAPIHelper/WSHelper";
import { getNow } from "@/modules/SinWave";

import { AppState } from "@/modules/SubSpeller/AppState";
import { sleep } from "@/modules/Time";
// import { NextSSVP } from "@/modules/SubSpeller/NextSSVP";
import { UserText } from "@/modules/SubSpeller/UserText";
// import {choise} from "@/modules/Random.js"

import { restAPIPost } from "@/modules/RestAPIHelper/RestAPIHelper";
import {HOST_CONFIG,getSecureProtocol} from "@/modules/HOST"
import { defineComponent,ref } from "vue"
import {experimentConfigDefault,OfflineCommand} from "@/modules/experimentConfig/configs"

export default defineComponent({
  setup() {
    let canvas:HTMLCanvasElement|undefined
    let ctx:CanvasRenderingContext2D|undefined
    let appState:AppState|undefined
    const userText:string[] = []
    let ws:WebSocket|undefined
    let begin_time = 0
    let p_id = ""
    let DBConfigStatus = ref("")
    let DBConfig = `{
  "current_participant_id" : "AXXSXX"
}`
    let P300Config =  `
{
  "spawn":200,
  "ttl":200
}
      
      `
    let ExperimentConfigOffline = JSON.stringify(experimentConfigDefault,null, 4)
    return {
      canvas,
      ctx,
      appState,
      userText,
      ws,
      begin_time,
      p_id,
      DBConfigStatus,
      DBConfig,

      P300Config,
      ExperimentConfigOffline,
    };
  },

  mounted() {
    this.canvas = document.getElementById("canvas")! as HTMLCanvasElement;
    this.ctx = this.canvas.getContext("2d")!;
  },
  computed: {
    mode() {
      return this.$route.params.mode;
    },
  },
  methods: {
    fullScreen() {
      this.canvas!.requestFullscreen();
      setTimeout(() => {
        this.run();
      }, 500);
    },
    async submitDBConfig() {
      
      let config = JSON.parse(this.DBConfig);
      this.p_id  = config["current_participant_id"]
    
      await restAPIPost(
        `http${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${HOST_CONFIG.ML_SERVER_PORT}/db`,
        {
          current_mode: this.mode,
          current_participant_id: this.p_id,
        },
        () => {
        
          this.DBConfigStatus = "okay";
        },
        () => {
          this.DBConfigStatus = "error";
        }
      );
    },
    run() {
      if (this.mode === "online") {
        this.setUpWSOnline();
      }
      if (this.mode === "offline") {
        this.setUpWSOffline();
      }

      this.canvas!.width = getSizeW(1) as number;
      this.canvas!.height = getSizeH(1) as number;

      let P300Config = JSON.parse(this.P300Config);

      this.appState = new AppState(
        this,
        P300Config["spawn"],
        P300Config["ttl"]
      );

      // const nextBtn = new NextSSVP(getSizeW(.55),getSizeH(.9),this.appState)

      const tick = () => {
        setBG(this);
        UserText.render(this, this.userText.join(","));
        // nextBtn.render(this)
        this.appState!.subSpellers.forEach((subSpeller) => {
          subSpeller.render(this);
        });

        window.requestAnimationFrame(tick);
      };
      tick();
    },
    setUpWSOnline() {
      this.ws = new WebSocket(`ws${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${HOST_CONFIG.ML_SERVER_PORT}/begin_online_mode/${this.p_id}`);
      this.ws.onmessage = async (incomingMSG) => {
        let msg = getJsonFromWSMessage(incomingMSG);
        if (msg["cmd"] == "next") {
          await sleep(1000);
          this.begin_time = getNow();
          this.appState!.toFlashingP300();
          await sleep(3000);
          this.appState!.toZERO();
          this.ws!.send(
            JSON.stringify({
              begin_time: this.begin_time,
            })
          );
        }
        if (msg["cmd"] == "output_model") {
          let alp = this.appState!.findAlphabetByIndex(
            msg.guessed_grid!,
            msg.guessed_index!
          );
          this.userText.push(alp);
        }
      };
    },
    setUpWSOffline() {
      let experimentConfig = JSON.parse(this.ExperimentConfigOffline);

      let cmds:OfflineCommand[] = []
      for(let round=0;round<experimentConfig['repeat'];round++){
        for(let i=0;i<experimentConfig['cmds'].length;i++){
          for(let j=0;j<experimentConfig['cmds'][i]['repeat'];j++){

          let {cmd,details} = experimentConfig['cmds'][i]
          cmds = [...cmds,new OfflineCommand(cmd,details)]
          }
        }

      }
     
      this.ws = new WebSocket(`ws${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${HOST_CONFIG.ML_SERVER_PORT}/begin_offline_mode/${this.p_id}`);

      this.ws.onmessage = async (incomingMSG) => {
        let msg = getJsonFromWSMessage(incomingMSG);

        if (msg["cmd"] == "next") {
                let currentCMD = cmds.shift()!

                if(currentCMD['cmd']=="sleep"){
                      let time= currentCMD["details"]["time"]
                      console.log(`sleep for ${time}`)
                      while(time>0){
                        time = time -1000
                     
                        await sleep(1000)
                        console.log(1)
                      }
                      currentCMD = cmds.shift()!

                }
           

                    if(currentCMD['cmd']=="target"){

                      let target = currentCMD['details']

                      let msgExperiment = {
                      target_grid: target['gridIndex'],
                      terget_index: target['alpIndex'],
                      data: [],
                      };
                      await sleep(1000);
                      this.appState!.toTarget(target, msgExperiment);
                      await sleep(1000);
                      this.appState!.toZERO();
                      await sleep(1000);
                      this.appState!.toFlashingP300();
                      await sleep(3000);
                      this.appState!.toZERO();
                      this.appState!.doneRound();
                      console.log(msgExperiment);
                      this.ws!.send(JSON.stringify(msgExperiment));
                    }
                   

                }
                

            }


              
          }   
         
         
          
          
        }
    

});
</script>
<style lang="scss" scoped>
</style>