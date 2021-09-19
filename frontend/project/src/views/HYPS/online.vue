<template lang="">
    <div class="main">
        <div class="grid">
        <SubSpeller :labels="['ภ','ถ','-ุ','-ู','ๆ','ไ','ฎ',' ำ','ฑ']" />
        <SubSpeller :labels="['-ึ','ค','พ', 'ธ', 'ะ', '-ํ', '-ั',  '-๊', '-ี', ]" />
        <SubSpeller :labels="['ต', 'จ', 'ข', 'ณ', 'ฯ', 'ญ', 'ร', 'น', 'ย']" />
        <SubSpeller :labels="['ฐ', 'ช', 'ฅ', 'บ', 'ล', 'ฃ', '.', 'ง', ',']" />

        <SubSpeller :labels="['ฤ', 'ฆ', 'ฏ', 'ฟ', 'ห', '(', ')', 'ผ', 'ป']" />
        <SubSpeller :labels="['ก', 'โ', 'ฌ','ด','เ','ฉ', 'ฮ', 'แ', 'อ']" />
        <SubSpeller :labels="['-็', '-๋', 'ษ', '-้', '-่', 'า', '-ฺ', '-ิ', '-์']" />
        <SubSpeller :labels="['ฒ', 'ศ', 'ซ', 'ส', 'ว', 'ฬ', '-ื', 'ท', 'ม']" />

        <div></div>
        <div></div>
        <SubSpeller :labels="['ฦ', 'ฝ', 'ใ', '0','DEL']" numCol="2" />
        <SubSpeller :labels="['7', '8', '9', '4', '5', '6', '1', '2', '3']" />


        </div>
     
          

    </div>
</template>
<script>
export default {
    components:{
        'SubSpeller': ()=>import("../../components/SubSpeller/SubSpeller.vue"),
    
    },
    mounted() {
      
    },
}
</script>

<style lang="scss" scoped>
.main{
    background-color: black;
    width: 100vw;
    height: 100vh;
   
}
.grid{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 1rem;
    padding: 2rem;
}
</style>
