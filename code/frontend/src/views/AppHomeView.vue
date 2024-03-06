<template>
  <div class="home-div">
    <h1 style="text-align: center">
      <span>Welcome to</span><br /><span>Online Support Ticket System</span>
    </h1>
    <b-row align-h="end">
      <b-button
        style="margin: 10px; margin-right: 50px"
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
.home-div {
  background-image: url("../assets/home_page_image.jpg");
  height: 100vh;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
</style>
