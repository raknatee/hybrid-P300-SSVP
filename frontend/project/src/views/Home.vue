<template>
  <div class="home">
    <!-- <router-link to="/hyps">hybrid-P300-SSVP</router-link> -->
    <headset/>
    <button @click="goOnline" >hybrid-P300-SSVP-Online mode</button>
    <br>
    <button @click="goOffline">hybrid-P300-SSVP-Offline mode</button>
  </div>
</template>

<script>
// @ is an alias to /src


export default {
  name: 'Home',
   components:{
    'headset': ()=>import("@/components/headset-status/HeadsetStatus.vue")
  },
  methods: {
    goOnline(){
      this.$router.push("/hyps/online")
    },
    goOffline(){
      this.$router.push("/hyps/offline")

    }
  },

}
</script>
