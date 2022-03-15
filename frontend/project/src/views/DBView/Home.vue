<template lang="">
     
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
            setInterval(()=>{
                backgroundColor.value="bg-green"
                clickFetch()
            },intervalTime)
        }

        return {databaseInfo,clickFetch,intervalTime,createIntervalFunc,backgroundColor}

    },
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
</style>