<template lang="">
        
        <div class="ch-display">
        <div class="highcharts" v-for="i in 8" :key="i" :id="`highcharts-container-ch${i-1}`"></div>
        <div class="highcharts" id="highcharts-container"></div>

        </div>
        
        <div class="interval-btn" :class="backgroundColor">
            <button @click="createIntervalFunc">set interval fetch for</button>
            <input type="number" v-model="intervalTime">
            <p>ms</p>
        </div>

        <button @click.prevent="clickFetch">fetch by hand</button>
    <p v-for="(value,key) in databaseInfo" :key="(value,key)">{{key}} {{value}}</p>
</template>
<script land="ts">
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

        let fsGraph;
        let chs = [];
        const chData = [
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
        ] 
        
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
            fsGraph.addPoint(data,true,true)
        }
        Highcharts.chart('highcharts-container',{
            title: {
                text:`${p_id} FS`
            },
            chart:{
                events:{
                    load: function(){
                        this.series.forEach((series)=>{
                            fsGraph=series
                        })
                        
                        
                    } 
                    
                }
            },
            series:[
                {name:"len",data:Array(7).fill(0)},
               
            ]
        })
        // await sleep(1000)
        for(let i=0;i<8;i++){
            const this_chart = Highcharts.chart(`highcharts-container-ch${i}`
            ,{
                title:{
                    text:`${p_id} ch${i}`
                },
                series:[
                    {name:"eeg",data:Array(300).fill(0)}
                ]
            }
            )
            chs.push(this_chart)
        }
        const wsFull = new WebSocket(`ws${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${
          HOST_CONFIG.ML_SERVER_PORT
        }/eeg_offline/${p_id}`
        );
        wsFull.onopen = ()=>{
            wsFull.send("RECEIVER_FULL")
        }
        wsFull.onmessage = (incomingMSG)=>{
            let msg = getJsonFromWSMessage(incomingMSG)
            let data = msg['data'];
            
      
            
            for(let ch=0;ch<8;ch++){

                chData[ch] = [...chData[ch],...data[ch]]
                chData[ch] = chData[ch].slice(-1250)
                const result = chData[ch]
                chs[ch].series[0].setData(result)
               
            }
            
            
        }
       
        
        
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
.ch-display{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
}
// .highcharts{
//     height: 30vh;
// }
// #chartJS{
//     height: 10vh;
// }
</style>