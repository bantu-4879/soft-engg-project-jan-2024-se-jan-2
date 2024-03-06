<template>
  <div>
    <UserNavbar :id_="id_"></UserNavbar>

    <b-container fluid="xl">
      <b-row>
        <b-col cols="12" sm="12" md="12">
          <h3 style="text-align: center">Frequently Asked Questions</h3>
          <b-row>
            <b-col cols="5" sm="12" md="5">
              <Tagging @tags_changed="onTagsChanged"></Tagging>
            </b-col>
            <b-col cols="5" sm="12" md="5">
              <b-form-group>
                <label for="input-query">Search Query:</label>
                <b-form-input
                  id="input-query"
                  v-model="query"
                  type="text"
                  placeholder="Enter search query"
                  :state="check_query"
                  aria-describedby="input-live-feedback-query"
                ></b-form-input> </b-form-group
            ></b-col>
            <b-col cols="2" sm="12" md="2" align-self="center">
              <b-form @reset="onReset" v-if="show" v-show="false">
                <b-button style="margin: 10px" type="reset" variant="danger">Reset</b-button>
              </b-form>
            </b-col>
          </b-row>
          <div style="height: 550px; overflow: auto; padding: 10px">
            <div v-for="faq in filtered_faq_card_details" :key="faq.faq_id">
              <FAQCard
                :faq_id="faq.faq_id"
                :question="faq.question"
                :answer="faq.solution"
                :attachments="faq.attachments"
              ></FAQCard>
            </div>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import FAQCard from "../components/FAQCard.vue";
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import Tagging from "../components/Tagging.vue";

export default {
  name: "CommonFAQs",
  components: { UserNavbar, FAQCard, Tagging },
  data() {
    return {
      id_: null,
      user_id: this.$store.getters.get_user_id,
      faq_card_details: [],
      filtered_faq_card_details: [],
      filter_tags: [],
      query: "",
      show: true,
    };
  },
  created() {
    let user_role = this.$store.getters.get_user_role;
    if (user_role == "student") {
      this.id_ = 4;
    }
    if (user_role == "support") {
      this.id_ = 3;
    }
    if (user_role == "admin") {
      this.id_ = 4;
    }
    let form = {
      filter_status: ["pending"],
    };
    let params = "";
    params = new URLSearchParams(form).toString();

    fetch(common.FAQ_API, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        web_token: this.$store.getters.get_web_token,
        user_id: this.user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.category == "success") {
          this.flashMessage.success({
            message: `Total ${data.message.length} FAQs retrieved.`,
          });
          this.faq_card_details = data.message;
          this.filtered_faq_card_details = data.message;
        }
        if (data.category == "error") {
          this.flashMessage.error({
            message: data.message,
          });
        }
      })
      .catch((error) => {
        this.$log.error(`Error : ${error}`);
        this.flashMessage.error({
          message: "Internal Server Error",
        });
      });
  },
  mounted() {},
  methods: {
    onTagsChanged(value) {
      this.filter_tags = value;
    },
    onReset(event) {
      if (event && event.preventDefault) {
        event.preventDefault();
      }
      // this.filtered_faq_card_details = this.faq_card_details;
      this.filter_tags = [];
      this.query = "";
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
      this.$forceUpdate();
    },
    filterCards() {
      // filtered_faq_card_details
      this.query = this.query.toLowerCase();
      this.filtered_faq_card_details = [];
      for (let i = 0; i < this.faq_card_details.length; i++) {
        let card = this.faq_card_details[i];
        let q = card.question.toLowerCase();
        let a = card.solution.toLowerCase();
        if (q.includes(this.query) || a.includes(this.query)) {
          this.filtered_faq_card_details.push(card);
        }
      }
      if (this.filter_tags.length > 0) {
        let temp_list = [];
        for (let i = 0; i < this.filtered_faq_card_details.length; i++) {
          let card = this.filtered_faq_card_details[i];
          if (
            this.filter_tags.includes(card.tag_1) ||
            this.filter_tags.includes(card.tag_2) ||
            this.filter_tags.includes(card.tag_3)
          ) {
            temp_list.push(card);
          }
        }
        this.filtered_faq_card_details = temp_list;
      }

      this.$forceUpdate();
    },
  },
  computed: {
    check_query() {
      // not being used in dev stage
      return this.query.length > 0 ? true : true;
    },
  },
  watch: {
    filter_tags: {
      handler: function (newValue, oldValue) {
        // Note: this is a deep watcher
        this.filterCards();
      },
      deep: true,
    },
    query: {
      handler: function (newValue, oldValue) {
        // Note: this is a deep watcher
        this.filterCards();
      },
      deep: true,
    },
  },
};
</script>

<style></style>
