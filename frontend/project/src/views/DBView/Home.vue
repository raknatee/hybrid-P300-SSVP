<template lang="">
    <div>
        <p>Currently, I havent implemented an auto refrech. Please click this below button by yourself.</p>
        <button @click.prevent="fetchAPI">fetch</button>
        <p v-for="(value,key) in databaseInfo" :key="(value,key)">{{key}} {{value}}</p>
    </div>
</template>
<script>

import { restAPIGet } from "@/modules/RestAPIHelper/RestAPIHelper.js";
import {HOST_CONFIG,getSecureProtocol} from "@/modules/HOST.js"
export default {
    data(){
        return{
            databaseInfo:null
        }
    },
    methods: {
        async fetchAPI(){
            let data = await restAPIGet(
                `http${getSecureProtocol()}://${HOST_CONFIG.ML_SERVER_HOSTNAME}:${HOST_CONFIG.ML_SERVER_PORT}/db/EEG-Database`
            )
            this.databaseInfo = data
        }
    },
}
</script>
<style lang="">
    
</style>