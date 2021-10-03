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
      
       
        <button @click="fullScreen">click me for fullscreen and run the experiment</button>
        
        <canvas id="canvas"></canvas>
    </div>
</template>
<script>
import { setBG } from "@/modules/renderer/BasicSetup.js";
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing.js";

import { getJsonFromWSMessage } from "@/modules/RestAPIHelper/WSHelper.js";
import { getNow } from "@/modules/SinWave.js";

import { AppState } from "@/modules/SubSpeller/AppState.js";
import { sleep } from "@/modules/Time.js";
// import { NextSSVP } from "@/modules/SubSpeller/NextSSVP.js";
import { UserText } from "@/modules/SubSpeller/UserText.js";
// import {choise} from "@/modules/Random.js"
import { repeat } from "@/modules/ArrayHelper.js";
import { restAPIPost } from "@/modules/RestAPIHelper/RestAPIHelper.js";

export default {
  data() {
    return {
      canvas: null,
      ctx: null,
      appState: null,
      userText: [],
      ws: null,
      begin_time: null,
      p_id: "",
      DBConfigStatus: "",
      DBConfig: `
{
  "current_participant_id" : "SXX"
}
      `,

      P300Config: `
{
  "spawn":200,
  "ttl":200
}
      
      `,
      ExperimentConfigOffline: `
{
  "targets":[
    {
      "target":{"gridIndex":2,"alpIndex":2},
      "repeat": 3
    },
    {
      "target":{ "gridIndex": 10, "alpIndex": 1 },
      "repeat": 3
    },
    {
      "target":{ "gridIndex": 11, "alpIndex": 8 },
      "repeat": 3
    }
  ],
  "repeat": 2
}
      
      `,
    };
  },

  mounted() {
    this.canvas = document.getElementById("canvas");
    this.ctx = this.canvas.getContext("2d");
  },
  computed: {
    mode() {
      return this.$route.params.mode;
    },
  },
  methods: {
    fullScreen() {
      this.canvas.requestFullscreen();
      setTimeout(() => {
        this.run();
      }, 500);
    },
    async submitDBConfig() {
      let config = JSON.parse(this.DBConfig);
      this.p_id  = config["current_participant_id"]
    
      await restAPIPost(
        "http://localhost:8000/db",
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
      this.canvas.width = getSizeW(1);
      this.canvas.height = getSizeH(1);

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
        this.appState.subSpellers.forEach((subSpeller) => {
          subSpeller.render(this);
        });

        window.requestAnimationFrame(tick);
      };
      tick();
    },
    setUpWSOnline() {
      this.ws = new WebSocket(`ws://localhost:8000/begin_online_mode/${this.p_id}`);
      this.ws.onmessage = async (msg) => {
        msg = getJsonFromWSMessage(msg);
        if (msg["cmd"] == "next") {
          await sleep(1000);
          this.begin_time = getNow();
          this.appState.toFlashingP300();
          await sleep(3000);
          this.appState.toZERO();
          this.ws.send(
            JSON.stringify({
              begin_time: this.begin_time,
            })
          );
        }
        if (msg["cmd"] == "output_model") {
          let alp = this.appState.findAlphabetByIndex(
            msg["guessed_grid"],
            msg["guessed_index"]
          );
          this.userText.push(alp);
        }
      };
    },
    setUpWSOffline() {
      let ExperimentConfig = JSON.parse(this.ExperimentConfigOffline);
      let targets = [];

      for (let i = 0; i < ExperimentConfig["targets"].length; i++) {
        let currentTargetObject = ExperimentConfig["targets"][i];
        targets.push(
          ...repeat(
            [currentTargetObject["target"]],
            currentTargetObject["repeat"]
          )
        );
      }

      targets = repeat(targets, ExperimentConfig["repeat"]);

      this.ws = new WebSocket(`ws://localhost:8000/begin_offline_mode/${this.p_id}`);
      this.ws.onmessage = async (msg) => {
        msg = getJsonFromWSMessage(msg);

        if (msg["cmd"] == "next") {
          if (targets.length <= 0) {
            this.ws.close();
            console.log("done the experiment");
            return;
          }
          let target = targets.shift();

          let msgExperiment = {
            target_grid: target.gridIndex,
            terget_index: target.alpIndex,
            data: [],
          };
          await sleep(1000);
          this.appState.toTarget(target, msgExperiment);
          await sleep(1000);
          this.appState.toZERO();
          await sleep(1000);
          this.appState.toFlashingP300();
          await sleep(3000);
          this.appState.toZERO();
          this.appState.doneRound();
          console.log(msgExperiment);
          this.ws.send(JSON.stringify(msgExperiment));
        }
      };
    },
  },
};
</script>
<style lang="scss" scoped>
</style>