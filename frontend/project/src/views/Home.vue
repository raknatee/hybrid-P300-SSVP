<template>
  <div class="home">
   <button @click="goOnline" >hybrid-P300-SSVP-Online mode</button>
    <br>
    <button @click="goOffline">hybrid-P300-SSVP-Offline mode</button>
    <br>
    <router-link :to="{path:'/dbview'}">Database viewer</router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "Home",
  methods: {
    goOnline(){
      this.$router.push("/hyps/online")
    },
    goOffline(){
      this.$router.push("/hyps/offline")
    }
  },
});
</script>
