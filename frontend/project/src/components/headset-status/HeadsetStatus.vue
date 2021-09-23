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
            status:'-'
        }
    },
    mounted() {
        setInterval(async()=>{
            let resp = await restAPIGet('http://localhost:8000/check_headset/')
            this.status = resp.status
        },4000)
    },
}
</script>
<style lang="">
    
</style>