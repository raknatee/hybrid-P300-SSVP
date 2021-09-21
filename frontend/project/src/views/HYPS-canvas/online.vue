<template lang="">
    <div class="layout">
        <button @click="fullScreen">click me for fullscreen</button>
        <canvas id="canvas"></canvas>
    </div>
</template>
<script>
import { setBG } from "@/modules/renderer/BasicSetup.js";
import { getSizeW, getSizeH } from "@/modules/renderer/Sizing.js";
import { SubSpeller } from "@/modules/SubSpeller/SubSpeller.js";
import { NextSSVP } from "@/modules/SubSpeller/NextSSVP.js";
import { GridHelper } from "@/modules/renderer/GridHelper.js";
import { style } from "@/modules/renderer/Style.js";

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
          subSpellers.push(null);
          continue;
        }
        let coor = gridHelper.getCoordinate(i);
        subSpellers.push(new SubSpeller(i, coor.x, coor.y));
      }

      const nextBtn = new NextSSVP(getSizeW(.55),getSizeH(.9))
      const tick = () => {
        setBG(this);
        // nextBtn.renderFlash(this)
        nextBtn.render(this)
        for (let i = 0; i < 12; i++) {
          let subSpeller = subSpellers[i];
          if (subSpeller === null) {
            continue;
          }

          // subSpeller.renderFlash(this);
          subSpeller.render(this);
        }

        window.requestAnimationFrame(tick);
      };
      tick();
    },
  },
};
</script>
<style lang="scss" scoped>
</style>