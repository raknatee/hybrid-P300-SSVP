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
        <p>Config the Experiment. PS. I provided the template please click below</p>

        <div v-if="mode=='offline'">
            <button @click="applyFullHYPS" >Full Offline HYPS</button>
        <button @click="applyOnlySSVP" >Only SSVP</button>
        </div>

      
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
import { SysText } from "@/modules/SubSpeller/SysText"
// import {choise} from "@/modules/Random.js"

import { restAPIPost } from "@/modules/RestAPIHelper/RestAPIHelper";
import {HOST_CONFIG,getSecureProtocol} from "@/modules/HOST"
import { defineComponent,ref } from "vue"
import {experimentConfigDefault,RuntimeCommand} from "./experimentConfig/configs"
import {HYPSCommands,DBConfig, CommandType, SleepDetails, TargetDetails} from "./experimentConfig/ConfigType"
import {ssvpConfig} from "./experimentConfig/SSVPConfig/experimentDefault"
export default defineComponent({
  setup() {
    let canvas:HTMLCanvasElement|undefined
    let ctx:CanvasRenderingContext2D|undefined
    let appState:AppState|undefined
    const userText:string[] = []
    let sysText = ""
  
    let ws:WebSocket|undefined
    let begin_time = 0
    let p_id = ""
    let DBConfigStatus = ref("")
    let DBConfig = JSON.stringify({"current_participant_id" : "AXXSXX"},null,4)
    let P300Config = ref("")
    let ExperimentConfigOffline = ref("")
    const applyFullHYPS = () =>{
      ExperimentConfigOffline.value = JSON.stringify(experimentConfigDefault,null, 4)
      P300Config.value = JSON.stringify({"spawn":200,"ttl":200},null,4)
    }
    const applyOnlySSVP = () =>{
      ExperimentConfigOffline.value = JSON.stringify(ssvpConfig,null, 4)
      P300Config.value = JSON.stringify({"spawn":0,"ttl":800},null,4)
    }
    return {
      canvas,
      ctx,
      appState,
      userText,
      sysText,
      ws,
      begin_time,
      p_id,
      DBConfigStatus,
      DBConfig,

      P300Config,
      ExperimentConfigOffline,
      applyFullHYPS,
      applyOnlySSVP
    };
  },

  mounted() {
    this.canvas = document.getElementById("canvas")! as HTMLCanvasElement;
    this.ctx = this.canvas.getContext("2d")!;

    if(this.mode=="online"){
      this.P300Config = JSON.stringify({"spawn":200,"ttl":200},null,4)
    }
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
      
      let config = JSON.parse(this.DBConfig) as DBConfig;
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

      this.canvas!.width = getSizeW(1) ;
      this.canvas!.height = getSizeH(1) ;

      let P300Config = JSON.parse(this.P300Config);

      this.appState = new AppState(
        this.canvas!,
        this.ctx!,
        P300Config["spawn"],
        P300Config["ttl"]
      );

      // const nextBtn = new NextSSVP(getSizeW(.55),getSizeH(.9),this.appState)

      const tick = () => {
        setBG(this);
        UserText.render(this.ctx!, this.userText.join(","));
        SysText.render(this.ctx!,this.sysText)
        // nextBtn.render(this)
        this.appState!.subSpellers.forEach((subSpeller) => {
          subSpeller.render(this.ctx!);
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
          let alp = this.appState!.findAlphabetByIndexOrder(
            msg.guessed_grid!,
            msg.guessed_index_order!
          );
          this.userText.push(alp);
        }
      };
    },
    setUpWSOffline() {
      let experimentConfig = JSON.parse(this.ExperimentConfigOffline) as HYPSCommands;

      let cmds:RuntimeCommand[] = []
      for(let round=0;round<experimentConfig['repeat'];round++){
        for(let i=0;i<experimentConfig['cmds'].length;i++){
          for(let j=0;j<experimentConfig['cmds'][i]['repeat'];j++){

          let {cmd,details} = experimentConfig['cmds'][i]
          cmds = [...cmds,new RuntimeCommand(cmd,details)]
          }
        }

      }
      
      this.ws = new WebSocket(`ws${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${HOST_CONFIG.ML_SERVER_PORT}/begin_offline_mode/${this.p_id}`);

      this.ws.onmessage = async (incomingMSG) => {
        let msg = getJsonFromWSMessage(incomingMSG);

        if (msg["cmd"] == "next") {
                this.userText= []
                this.userText.push(cmds.length.toString())
                let currentCMD = cmds.shift()!

                if(currentCMD['cmd'] === CommandType.sleep){

                      let details = currentCMD["details"] as SleepDetails
                      let time= details["time"]
                      console.log(`sleep for ${time}`)
                      while(time>0){
                        this.sysText = (time/1000).toString()
                        time = time -1000
                     
                        await sleep(1000)
                   
                      }
                      this.sysText = ""
                      this.userText= []
                      this.userText.push(cmds.length.toString())
                      currentCMD = cmds.shift()!

                }
           

                    if(currentCMD['cmd'] === CommandType.target){

                      let target = currentCMD['details'] as TargetDetails

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
                      await sleep(2000);
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