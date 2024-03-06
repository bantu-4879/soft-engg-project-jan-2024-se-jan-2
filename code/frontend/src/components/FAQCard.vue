<template>
  <div>
    <b-container class="faq-card-container">
      <b-row class="row" @click="questionClicked">
        <b-col class="col" cols="1" lg="1" sm="1">
          <b-button variant="info">
            <b-icon icon="question-octagon" font-scale="1.5"></b-icon>
          </b-button>
        </b-col>
        <b-col class="col" cols="11" lg="11" sm="11">{{ question }}</b-col>
      </b-row>

      <b-row class="row" v-show="show_answer" @click="questionClicked">
        <b-col class="col" cols="1" lg="1" sm="1">
          <b>
            <i>Solution:</i>
          </b>
        </b-col>
        <b-col class="col" cols="11" lg="11" sm="11">
          <p>{{ answer }}</p>
          <div v-show="attachments.length > 0">
            <p>Attachments:</p>
            <div v-for="(attach, imageIndex) in attachments" :key="imageIndex">
              <img :src="attach.attachment_loc" class="img-fluid" />
            </div>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "FAQCard",
  props: ["faq_id", "question", "answer", "attachments"],
  components: {},
  data() {
    return {
      show_answer: false,
    };
  },
  mounted() {},
  methods: {
    questionClicked() {
      this.show_answer = !this.show_answer;
    },
  },
  computed: {},
};
</script>

<style scoped>
.faq-card-container {
  box-shadow: 2px 4px 5px 5px #dbdada;
  background-color: rgb(251, 252, 252);
  margin: 12px 5px;
  padding: 10px;
}
.faq-card-container:hover {
  box-shadow: 5px 8px 8px 10px #888888;
  background-color: rgb(255, 255, 255);
}
.row {
  padding-top: 5px;
  padding-bottom: 5px;
}
.faq-card-buttons {
  border-color: #ffffff;
}
.faq-card-buttons:hover {
  border-color: #95ddfa;
  box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19);
}
</style>
