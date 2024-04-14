<template>
  <div class="home-div">
    <div class="home-div-heading">
      <h1 style="text-align: center; margin-top: 50px;">
        <span>Welcome to</span><br /><span>Ticket System Integration with Discourse and Webhooks</span>
      </h1>
    </div>
    <b-row align-h="center" style="margin-top: 20em;">
      <b-button
        style="margin: 10px; margin-right: 10px"
        type="button"
        variant="primary"
        :to="{ path: '/login' }"
        >Login</b-button
      ></b-row
    >
  </div>
</template>

<script>
import * as common from "../assets/common.js";

export default {
  name: "AppHomeView",
  components: {},
  data() {
    return {
      show: true,
    };
  },
  methods: {},
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Antic+Didone&display=swap');

.home-div {
  background-image: url("../assets/pasqal_logo.jpeg");
  height: 75vh;
  background-position: center;
  background-repeat: no-repeat;
  
}

.home-div-heading{
  font-family: 'Antic Didone', serif;
}
</style>
