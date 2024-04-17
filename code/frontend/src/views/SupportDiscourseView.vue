<template>
    <div>
      <user-navbar></user-navbar>
      <div class="container mt-4">
        <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="6" md="12" style="border-right: dashed black">
          <h3 style="text-align: center">Discourse Topics from Ticket Resolution System </h3>
          <div v-if="isLoading" class="text-center mt-4">
          <b-spinner></b-spinner>
        </div>
        <div v-else>
          <div v-if="errorMessage" class="alert alert-danger mt-4">
            {{ errorMessage }}
          </div>
          <div v-else class="scrollable-container">
            <div v-if="topics.length > 0">
              <div v-for="topic in topics" :key="topic.id" class="card mb-3">
                <div class="card-body">
                  <h5 class="card-title">{{ topic.title }}</h5>
                  <div class="d-flex align-items-center">
                    <h6 class="card-subtitle">{{ topic.posts_count }}</h6><p>  </p>
                    <b-icon
                        icon="chat-right-quote-fill"
                        aria-hidden="true"
                        class="bg-light"
                        variant="danger"
                    ></b-icon>
                    </div>
                  <p class="card-text">
                    <small class="text-muted">Created At: {{ formatDateTime(topic.created_at) }}</small><br>
                    <small class="text-muted">Last Modified At: {{ formatDateTime(topic.last_modified_at) }}</small>
                  </p>
                </div>
              </div>
            </div>
            <div v-else class="mt-4">
              <p>No topics found.</p>
            </div>
          </div>
        </div>
        </b-col>
        <!--
        <b-col cols="12" sm="6" md="4">
          <b-row>
            <h3 style="text-align: center">Create Tags</h3>
          </b-row> <b-row>
            <h3 style="text-align: center">Create Subcategories</h3>
            <CreateSubcategory></CreateSubcategory>
          </b-row>
          
        </b-col>-->
      </b-row>
    </b-container>
      </div>
    </div>
  </template>
  
  <script>
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import CreateSubcategory from "../components/StaffCreateSubcategories.vue";

export default {
  name: "SupportDiscourse",
  components: { UserNavbar,CreateSubcategory },
  data() {
    return {
      user_id: this.$store.getters.get_user_id,
      isLoading: true,
      errorMessage: "",
      topics: [],
    };
  },
  created() {
    fetch(common.DISCOURSE_TICKET_API + '/category/topics', {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        webtoken: this.$store.getters.get_web_token,
        userid: this.user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        this.isLoading = false;
        if (data.category == "success") {
          this.topics = data.message;
          this.flashMessage.success({ message: "Discourse data retrieved." });
        }
        if (data.category == "error") {
          this.errorMessage = data.message;
          this.flashMessage.error({ message: data.message });
        }
      })
      .catch((error) => {
        this.isLoading = false;
        this.$log.error(`Error : ${error}`);
        this.flashMessage.error({ message: "Internal Server Error" });
      });
  },
  methods: {
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return "N/A";
      const dateTime = new Date(dateTimeString);
      return dateTime.toLocaleString();
    },
  },
};
</script>
  
  <style>
.scrollable-container {
  max-height: 600px; 
  overflow-y: auto;
}
</style>
  