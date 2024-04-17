<template>
    <div>
      <div v-if="loading">Loading...</div>
      <div v-else>
        <PostDetail :message="messages"></PostDetail>
      </div>
    </div>
  </template>
  
  <script>
  import PostDetail from './DiscoursePostDetails.vue'; // Import the DiscourseDetails component
  import * as common from "../assets/common.js";
  export default {
    name: 'Discourse',
    components: {
      PostDetail
    },
    props:['id'],
    data() {
      return {
        messages:null,
        loading:false,
        user_id:this.$store.getters.get_user_id,
      };
    },
    mounted() {
      this.fetchTopicDetails(); 
    },
    methods: {
        fetchTopicDetails() {
          this.loading = true;
          const url = `${common.DISCOURSE_TICKET_API}/topic/${this.user_id}/${this.id}`;
          fetch(url, {
            method:"GET",
            headers: {
              webtoken: this.$store.getters.get_web_token,
              userid: this.user_id,
            }
          })
          .then((response) => response.json())
          .then(data => {
            if (data.category === "success") {
                this.messages=data.message;
              this.flashMessage.success({ message: "Discourse Thread retrieved successfully." });
            } else if (data.category === "error") {
              this.flashMessage.error({ message: error.message });
            }
          })
          .catch(error => {
            this.$log.error(`Error : ${error}`);
            this.flashMessage.error({ message: "Discourse Topic does not exist." });
          });
          this.loading = false;
      }
    }
  };
  </script>
  