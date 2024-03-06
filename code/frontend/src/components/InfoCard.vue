<template>
  <div class="info-card-container">
    <b-card :title="value" :sub-title="title" bg-variant="light" class="text-center"> </b-card>
  </div>
</template>

<script>
export default {
  name: "InfoCard",
  props: ["title", "value"],
  components: {},
  data() {
    return {};
  },
  created() {},
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style scoped>
.info-card-container {
  box-shadow: 2px 4px 5px 5px #dbdada;
  margin: 12px 15px;
}
</style>
