<template lang="">
    <div class="grid" :style="gridCol" ref="subGrid">
     
      <alp v-for="label in labels" :label="label" :key="label" />
    </div>
</template>
<script>
// eslint-disable-next-line no-unused-vars
import {SinWave,getNow} from "@/modules/SinWave.js"
export default {
    props:{'labels':Array,numCol:{default: 3}},
    components:{
        'alp': ()=>import('./Alphabet/Alphabet.vue')
    },
    computed:{
        gridCol(){
            return `grid-template-columns: repeat(${this.numCol},1fr);`
        }
    },
    mounted() {
     
        // const thisWave = new SinWave(10,.5*Math.PI)
        // const tick = ()=>{
               
            
        //     if(thisWave.isUp(getNow())){
        //         console.log("up")
        //         this.$refs.subGrid.classList.add("up")
                
        //     }else{
               
        //         console.log("down")
        //         this.$refs.subGrid.classList.remove("up")

        //     }
        //     window.requestAnimationFrame(tick)
        // }
        // tick()
        
        
    },
}
</script>
<style lang="scss" scoped>
.grid{
    display: grid;

    padding: 0;
    font-size: 2rem;
    background-color: gray;
}
.up{
    background-color: rgb(187, 115, 115);
}
</style>