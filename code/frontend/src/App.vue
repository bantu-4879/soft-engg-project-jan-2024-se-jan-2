<template>
  <div id="app">
    <FlashMessage
      :position="'left bottom'"
      style="font-size: 15px; position: relative; z-index: 10000"
    />
    <router-view />
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {};
  },
  beforeCreate() {
    console.log("Creating app.");
    this.$store.commit("initialiseStore");
  },
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: start;
  color: #2c3e50;
}
</style>
