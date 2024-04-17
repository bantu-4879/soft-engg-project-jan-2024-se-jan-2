<!-- <template>
  <div class="info-card-container">
    <b-card
      :title="value"
      :sub-title="title"
      bg-variant="light"
      class="text-center"
    >
    </b-card>
  </div>
</template>

<script>
export default {
  name: "InfoCard",
  props: ["title", "value2", "value"],
  components: {
    delete_card: false,
  },
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
</style> -->

<template>
  <div class="info-card-container">
    <b-card :title="title" :sub-title="value2" bg-variant="light" class="info-card">
      <div class="info-value">{{ value }}</div>
    </b-card>
  </div>
</template>

<script>
export default {
  name: "InfoCard",
  props: ["title", "value2", "value"],
};
</script>

<style scoped>
.info-card-container {
  margin: 20px;
}

.info-card {
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.info-card .card-header {
  background-color: #4dd325; /* Green header color */
  color: #fff; /* White text color */
  border-radius: 10px 10px 0 0; /* Rounded top corners */
  padding: 10px 20px; /* Added padding for header */
}

.info-card .info-value {
  font-size: 36px; /* Increased font size for value */
  font-weight: bold;
  color: #333; /* Dark text color */
  padding: 20px;
}

.info-card .card-footer {
  background-color: #f8f9fa; /* Light footer color */
  border-radius: 0 0 10px 10px; /* Rounded bottom corners */
  padding: 10px 20px; /* Added padding for footer */
}
</style>