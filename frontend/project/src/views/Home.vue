<template>
  <div class="home">
    <router-link :to="{path:'/hyps/online'}">hybrid-P300-SSVP-Online mode</router-link>

   
    <br>
    <router-link :to="{path:'/hyps/offline'}">hybrid-P300-SSVP-Offline mode</router-link>

   
  

    <br>
    <router-link :to="{path:'/dbview'}">Database viewer</router-link>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
export default defineComponent({

 setup(){
   document.title= "Home Page"
 }


})
</script>

