<template>
  <div class="home">
    <!-- <router-link to="/hyps">hybrid-P300-SSVP</router-link> -->
    <button @click="go" id="hyps-btn">hybrid-P300-SSVP</button>
  </div>
</template>

<script>
// @ is an alias to /src


export default {
  name: 'Home',
  methods: {
    go(){
      //  document.body.requestFullscreen()
      this.$router.push("/hyps/online")
    }
  },

}
</script>
