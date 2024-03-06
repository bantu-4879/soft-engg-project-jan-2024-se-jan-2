<template>
  <div>
    <UserNavbar :id_="2"></UserNavbar>
    <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="6" md="6">
          <h3 style="text-align: center">New Students</h3>
          <div style="height: 550px; overflow: auto; padding: 10px">
            <div v-for="user in unverified_new_user" :key="user.user_id">
              <div v-if="user.role == 'student'">
                <UserCard
                  :n_user_id="user.user_id"
                  :first_name="user.first_name"
                  :last_name="user.last_name"
                  :email="user.email"
                  :role="user.role"
                  :show="true"
                ></UserCard>
              </div>
            </div>
          </div>
        </b-col>
        <b-col cols="12" sm="6" md="6" style="border-left: dashed black">
          <h3 style="text-align: center">New Support Staff</h3>
          <div style="height: 550px; overflow: auto; padding: 10px">
            <div v-for="user in unverified_new_user" :key="user.user_id">
              <div v-if="user.role == 'support'">
                <UserCard
                  :n_user_id="user.user_id"
                  :first_name="user.first_name"
                  :last_name="user.last_name"
                  :email="user.email"
                  :role="user.role"
                  :show="true"
                ></UserCard>
              </div>
            </div>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import TicketCard from "../components/TicketCard.vue";
import InfoCard from "../components/InfoCard.vue";
import UserCard from "../components/UserCard.vue";

export default {
  name: "AdminValidateUsers",
  components: { UserNavbar, UserCard },
  data() {
    return {
      user_id: this.$store.getters.get_user_id,
      unverified_new_user: [],
    };
  },
  created() {
    let form = {
      filter_status: ["pending"],
    };
    let params = "";
    params = new URLSearchParams(form).toString();

    fetch(common.AUTH_API_NEWUSERS, {
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
          this.unverified_new_user = data.message;
          if (this.unverified_new_user.length > 0) {
            this.flashMessage.success({
              message: `${this.unverified_new_user.length} unverified users found.`,
            });
          } else {
            this.flashMessage.success({
              message: "No unverified users present.",
            });
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
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style></style>
