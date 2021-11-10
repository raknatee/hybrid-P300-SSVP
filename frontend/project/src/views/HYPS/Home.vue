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
            <button @click="applyFullHYPS200200" >Full Offline HYPS 200,200</button>
            <button @click="applyFullHYPS100200" >Full Offline HYPS 100,200</button>
            <button @click="applyMiniHYPS300600" >Mini Offline HYPS 300,600</button>
        <button @click="applyOnlySSVP" >Only SSVP</button>
        </div>

      
        <h1>P300 Config</h1>
        <textarea v-model="P300ConfigString" rows="7" cols="50"></textarea>
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
import { getNow,getPerformanceNow } from "@/modules/Time";

import { AppState } from "@/modules/SubSpeller/AppState";
import { sleep } from "@/modules/Time";
// import { NextSSVP } from "@/modules/SubSpeller/NextSSVP";
import { UserText } from "@/modules/SubSpeller/UserText";
import { SysText } from "@/modules/SubSpeller/SysText";
import { FPSText } from "@/modules/SubSpeller/FPSText";
// import {choise} from "@/modules/Random.js"

import { restAPIPost } from "@/modules/RestAPIHelper/RestAPIHelper";
import { HOST_CONFIG, getSecureProtocol } from "@/modules/HOST";
import { defineComponent, ref } from "vue";
import {
  experimentConfigDefault,
  RuntimeCommand,
} from "./experimentConfig/configs";
import {FPS} from "@/modules/renderer/FPS"
import {
  HYPSCommands,
  DBConfig,
  CommandType,
  SleepDetails,
  TargetDetails,
  P300Config,
} from "./experimentConfig/ConfigType";
import { ssvpConfig } from "./experimentConfig/SSVPConfig/experimentDefault";
export default defineComponent({
  setup() {
    let canvas: HTMLCanvasElement | undefined;
    let ctx: CanvasRenderingContext2D | undefined;
    let appState: AppState | undefined;
    const userText: string[] = [];
    let sysText = "";

    let ws: WebSocket | undefined;
    let begin_time = 0;
    let p_id = "";
    let DBConfigStatus = ref("");
    let DBConfig = JSON.stringify(
      { current_participant_id: "AXXSXX" },
      null,
      4
    );
    let P300ConfigString = ref("");
    let ExperimentConfigOffline = ref("");
    const applyFullHYPS200200 = () => {
      ExperimentConfigOffline.value = JSON.stringify(
        experimentConfigDefault,
        null,
        4
      );
      const p300:P300Config = { spawn: 200, ttl: 200, time_per_round: 2000 }
      P300ConfigString.value = JSON.stringify(
        p300,
        null,
        4
      );
    };
      const applyFullHYPS100200 = () => {
      ExperimentConfigOffline.value = JSON.stringify(
        experimentConfigDefault,
        null,
        4
      );
      const p300:P300Config = { spawn: 100, ttl: 200, time_per_round: 1000 }
      P300ConfigString.value = JSON.stringify(
        p300,
        null,
        4
      );
    };
    const applyMiniHYPS300600 = () =>{
      ExperimentConfigOffline.value = JSON.stringify(ssvpConfig, null, 4);
       const p300:P300Config = { spawn: 300, ttl: 600, time_per_round: 3000 }
      P300ConfigString.value = JSON.stringify(
        p300,
        null,
        4
      );

    }
    const applyOnlySSVP = () => {
      const p300:P300Config ={ spawn: 0, ttl: 1000, time_per_round: 1000 }
      ExperimentConfigOffline.value = JSON.stringify(ssvpConfig, null, 4);
      P300ConfigString.value = JSON.stringify(
        p300,
        null,
        4
      );
    };

    const applyOnline = () => {
      const config: P300Config = {
        spawn: 100,
        ttl: 200,
        time_per_round: 1000,
      };
      P300ConfigString.value = JSON.stringify(config, null, 4);
    };
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

      P300ConfigString,
      ExperimentConfigOffline,
      applyFullHYPS200200,
      applyFullHYPS100200,
      applyMiniHYPS300600,
      applyOnlySSVP,
      applyOnline
    };
  },

  mounted() {
    this.canvas = document.getElementById("canvas")! as HTMLCanvasElement;
    this.ctx = this.canvas.getContext("2d",{alpha:false})!;
 
    if (this.mode == "online") {
      this.applyOnline()
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
      this.p_id = config["current_participant_id"];

      await restAPIPost(
        `http${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${
          HOST_CONFIG.ML_SERVER_PORT
        }/db`,
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
      let P300ConfigObject: P300Config = JSON.parse(this.P300ConfigString);

      if (this.mode === "online") {
        this.setUpWSOnline(P300ConfigObject.time_per_round);
      }
      if (this.mode === "offline") {
        this.setUpWSOffline(P300ConfigObject.time_per_round);
      }

      this.canvas!.width = getSizeW(1) ;
      this.canvas!.height = getSizeH(1) ;

      this.appState = new AppState(
        this.canvas!,
        this.ctx!,
        P300ConfigObject["spawn"],
        P300ConfigObject["ttl"]
      );

      // const nextBtn = new NextSSVP(getSizeW(.55),getSizeH(.9),this.appState)

      let previousTime = getPerformanceNow()
      const tick = () => {

      
        setBG(this.ctx!,this.canvas!.width,this.canvas!.height);

        FPSText.render(this.ctx!,FPS.get().toString())
        FPS.tick()
     

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
    setUpWSOnline(timePerRound: number) {
      this.ws = new WebSocket(
        `ws${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${
          HOST_CONFIG.ML_SERVER_PORT
        }/begin_online_mode/${this.p_id}`
      );
      this.ws.onmessage = async (incomingMSG) => {
        let msg = getJsonFromWSMessage(incomingMSG);
        if (msg["cmd"] == "next") {
          await sleep(1000);
          this.begin_time = getNow();
          this.appState!.toFlashingP300(timePerRound);
          await sleep(timePerRound);
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
    setUpWSOffline(timePerRound: number) {
      let experimentConfig = JSON.parse(
        this.ExperimentConfigOffline
      ) as HYPSCommands;

      let cmds: RuntimeCommand[] = [];
      for (let round = 0; round < experimentConfig["repeat"]; round++) {
        for (let i = 0; i < experimentConfig["cmds"].length; i++) {
          for (let j = 0; j < experimentConfig["cmds"][i]["repeat"]; j++) {
            let { cmd, details } = experimentConfig["cmds"][i];
            cmds = [...cmds, new RuntimeCommand(cmd, details)];
          }
        }
      }

      this.ws = new WebSocket(
        `ws${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${
          HOST_CONFIG.ML_SERVER_PORT
        }/begin_offline_mode/${this.p_id}`
      );

      this.ws.onmessage = async (incomingMSG) => {
        let msg = getJsonFromWSMessage(incomingMSG);

        if (msg["cmd"] == "next") {
          this.userText = [];
          this.userText.push(cmds.length.toString());
          let currentCMD = cmds.shift()!;

          if (currentCMD["cmd"] === CommandType.sleep) {
            let details = currentCMD["details"] as SleepDetails;
            let time = details["time"];
            console.log(`sleep for ${time}`);
            while (time > 0) {
              this.sysText = (time / 1000).toString();
              time = time - 1000;

              await sleep(1000);
            }
            this.sysText = "";
            this.userText = [];
            this.userText.push(cmds.length.toString());
            currentCMD = cmds.shift()!;
          }

          if (currentCMD["cmd"] === CommandType.target) {
            let target = currentCMD["details"] as TargetDetails;

            let msgExperiment = {
              target_grid: target["gridIndex"],
              terget_index: target["alpIndex"],
              data: [],
            };
            await sleep(1000);
            this.appState!.toTarget(target, msgExperiment);
            await sleep(1000);
            this.appState!.toZERO();
            await sleep(1000);
            this.appState!.toFlashingP300(timePerRound);
            await sleep(timePerRound);
            console.log("--------------------------------------")
            this.appState!.toZERO();
            this.appState!.doneRound();
            console.log(msgExperiment);
            this.ws!.send(JSON.stringify(msgExperiment));
          }
        }
      };
    },
  },
});
</script>
<style lang="scss" scoped>
</style>