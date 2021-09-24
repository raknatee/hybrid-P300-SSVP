<template lang="">
    <div class="grid" :style="gridCol" ref="subGrid">
     
      <alp v-for="label in labels" :label="label" :key="label" />
    </div>
</template>
<script>
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