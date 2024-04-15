<template>
  <div>
    <UserNavbar :id_="1"></UserNavbar>
    <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="5" md="12">
          <div
            class="info-card-container"
            v-for="message in messages_list"
            :key="message.id"
          >
            <b-card
              :title="message.message"
              :sub-title="message.received_at"
              bg-variant="light"
              class="text-center"
            >
              <b-button
                @click="delete_inbox_message(message.id)"
                v-show="delete_button == true"
                variant="danger"
                >Delete</b-button
              >
            </b-card>
          </div>
          <div
            class="info-card-container"
            v-for="message in discourse_messages_list"
            :key="message.id"
          >
            <b-card
              :title="message.slug"
              :sub-title="message.created_at"
              bg-variant="light"
              class="text-center"
            >
              <b-button
                @click="delete_inbox_message(message.id)"
                v-show="delete_button == true"
                variant="danger"
                >Delete</b-button
              >
            </b-card>
          </div>
        </b-col>
      </b-row>
    </b-container>

    <br />
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import InfoCard from "../components/InfoCard.vue";

export default {
  name: "InboxView",
  components: { UserNavbar, InfoCard },
  data() {
    return {
      user_id: this.$store.getters.get_user_id,
      messages_list: [],
      discourse_messages_list: [],
      delete_button: true,
    };
  },
  created() {
    let form = {
      filter_status: ["pending"],
    };
    let params = "";
    params = new URLSearchParams(form).toString();

    fetch(common.INBOX_API + `/${this.user_id}`, {
      //fetch(common.INBOX_API + "/23463b99b62a72f26ed677cc556c44e8", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        webtoken: this.$store.getters.get_web_token,
        userid: this.user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.category == "success") {
          this.flashMessage.success({
            message: "User Inbox Data retrieved.",
          });
          this.messages_list = data.message;
        }
        if (data.category == "error") {
          this.flashMessage.error({
            message: data.message,
          });
        }
        if (this.messages_list.length == 0) {
          this.delete_button = false;
          this.messages_list.push({
            message: "No New Messages!",
            recieved_at: "",
          });
        }
      })
      .catch((error) => {
        this.$log.error(`Error : ${error}`);
        this.flashMessage.error({
          message: "Internal Server Error",
        });
      });

    fetch(common.DISCOURSE_REGISTER_API + "/notifications" + `/${this.user_id}`, {
      //fetch(common.INBOX_API + "/23463b99b62a72f26ed677cc556c44e8", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        webtoken: this.$store.getters.get_web_token,
        userid: this.user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.category == "success") {
          this.flashMessage.success({
            message: "User Inbox Data retrieved.",
          });
          this.discourse_messages_list = data.message;
        }
        if (data.category == "error") {
          this.flashMessage.error({
            message: data.message,
          });
        }
        if (this.messages_list.length == 0) {
          this.delete_button = false;
          this.discourse_messages_list.push({
            message: "No New Discourse Messages!",
            recieved_at: "",
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
    delete_inbox_message: function (message_id) {
      console.log(message_id);
      fetch(common.INBOX_API + `/${this.user_id}/` + message_id, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          webtoken: this.$store.getters.get_web_token,
          userid: this.user_id,
        },
        body: JSON.stringify({
          user_id: this.user_id,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.flashMessage.success({
              message: "Message Deleted!",
            });
            for (let i = 0; i <= this.messages_list.length; i++) {
              if (this.messages_list[i].id == this.message_id) {
                this.messages_list.splice(i, 1);
              }
            }
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
  },
  computed: {},
};
</script>

<style scoped>
.info-card-container {
  box-shadow: 2px 4px 5px 5px #dbdada;
  margin: 12px 15px;
}
</style>
