<template lang="">
        <div class="highcharts" id="highcharts-container"></div>
        <div class="interval-btn" :class="backgroundColor">
            <button @click="createIntervalFunc">set interval fetch for</button>
            <input type="number" v-model="intervalTime">
            <p>ms</p>
        </div>

        <button @click.prevent="clickFetch">fetch by hand</button>
    <p v-for="(value,key) in databaseInfo" :key="(value,key)">{{key}} {{value}}</p>
</template>
<script>
import { restAPIGet } from "@/modules/RestAPIHelper/RestAPIHelper.ts";
import {HOST_CONFIG,getSecureProtocol} from "@/modules/HOST.ts"
import { defineComponent,ref } from "vue"
import { getJsonFromWSMessage } from "@/modules/RestAPIHelper/WSHelper";

import Highcharts from 'highcharts';
export default defineComponent({
    setup(){
        document.title="Database Viewer"
        let databaseInfo = ref("")
        const fetchAPI = async() =>{
            return await restAPIGet(
                `http${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${HOST_CONFIG.ML_SERVER_PORT}/db/EEG-Database`
            )
        }

        const clickFetch = async() =>{
            databaseInfo.value =  await fetchAPI()
        }
        
        let intervalTime = ref(2000)
        let backgroundColor = ref("bg-red")
        const createIntervalFunc = () =>{
            backgroundColor.value="bg-green"
            setInterval(()=>{
                clickFetch()
            },intervalTime.value)
        }

        return {databaseInfo,clickFetch,intervalTime,createIntervalFunc,backgroundColor}

    },
    async mounted(){
        const jsonOutput = await restAPIGet(`http${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${HOST_CONFIG.ML_SERVER_PORT}/db`)
        const p_id = jsonOutput['current_participant_id']
        let chs = [];
        const ws = new WebSocket(
        `ws${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${
          HOST_CONFIG.ML_SERVER_PORT
        }/eeg_offline/${p_id}`
        );
        ws.onopen = ()=>{
            ws.send("RECEIVER_LEN")
        }
        ws.onmessage = (incomingMSG)=>{
            let msg = getJsonFromWSMessage(incomingMSG)
            let data = msg['len']
            chs[0].addPoint(data,true,true)
            // for(let i=0;i<data.length;i++){
            //     for(let channel=0;channel<1;channel++){
            //         chs[channel].addPoint([data[i][channel]],true,true)
            //     }
            // }
        }
        Highcharts.chart('highcharts-container',{
            title: {
                text:`${p_id} FS`
            },
            chart:{
                events:{
                    load: function(){
                        this.series.forEach((series)=>{
                            chs.push(series)
                        })
                        
                        
                    } 
                    
                }
            },
            series:[
                {name:"len",data:Array(10).fill(0)},
               
            ]
        })
        
        
    }
})
</script>

<style lang="scss" scoped>
.interval-btn{
    display: flex;
    align-items: center;
    width: 20vw;
    input {
        width: 3rem;
    }
    p {
        color: aliceblue;
    }
}
.bg-red{
    background-color: rgb(196, 29, 29);
}
.bg-green{
    background-color: green;
}
.highcharts{
    height: 40vh;
}
</style>