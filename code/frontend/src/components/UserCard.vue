<template>
  <div class="user-card-container" v-if="this.show_component">
    <b-list-group>
      <b-list-group-item class="d-flex justify-content-between align-items-center">
        Name: {{ first_name }} {{ last_name }}
        <b-button @click="verify_user" variant="outline-light">
          <b-icon icon="check-square" scale="2" variant="success"></b-icon>
        </b-button>
      </b-list-group-item>
      <b-list-group-item class="d-flex justify-content-between align-items-center">
        Email: {{ email }}
        <b-button @click="not_verify_user" variant="outline-light">
          <b-icon icon="x-circle" scale="2" variant="danger"></b-icon>
        </b-button>
      </b-list-group-item>
    </b-list-group>
    <b-list-group-item class="d-flex justify-content-between align-items-center">
      Role: {{ role }}
    </b-list-group-item>
  </div>
</template>

<script>
import * as common from "../assets/common.js";
export default {
  name: "UserCard",
  props: ["n_user_id", "first_name", "last_name", "email", "role", "show"],
  components: {},
  data() {
    return {
      user_id: this.$store.getters.get_user_id,
      new_user_id: this.n_user_id,
      show_component: this.show,
    };
  },
  created() {},
  mounted() {},
  methods: {
    init() {
      this.new_user_id = this.n_user_id;
    },
    not_verify_user: async function (event) {
      fetch(common.AUTH_API_NEWUSERS + `/${this.new_user_id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          web_token: this.$store.getters.get_web_token,
          user_id: this.user_id,
        },
        body: JSON.stringify({
          user_id: this.new_user_id,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.flashMessage.success({
              message: "Verification Declined",
            });
            this.show_component = false;
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
    verify_user: async function (event) {
      event.preventDefault();

      fetch(common.AUTH_API_NEWUSERS + `/${this.new_user_id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          web_token: this.$store.getters.get_web_token,
          user_id: this.user_id,
        },
        body: JSON.stringify({
          user_id: this.new_user_id,
          verified: "true",
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.flashMessage.success({
              message: "Successfully Verified",
            });
            this.show_component = false;
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
.user-card-container {
  box-shadow: 2px 4px 5px 5px #dbdada;
  /* background-color: rgb(251, 252, 252); */
  margin: 12px 15px;
  /* padding: 10px; */
}
/* .info-card-container:hover {
  box-shadow: 5px 8px 8px 10px #888888;
   background-color: rgb(255, 255, 255); 
} */
</style>
