<template lang="">
    <div>
        <h1>HeadsetStatus</h1>
        <h2>Status: {{status}}</h2>
    </div>
</template>
<script>
import {restAPIGet} from "@/modules/RestAPIHelper/RestAPIHelper.js"
export default {
    data(){
        return {
            status:'-',
            interval:null
        }
    },
    mounted() {
        this.interval = setInterval(async()=>{
            let resp = await restAPIGet('http://localhost:8000/check_headset')
            this.status = resp.status
        },1000)
    },
    beforeDestroy() {
        console.log("clear check headset")
        clearInterval(this.interval)
    }
}
</script>
<style lang="">
    
</style>