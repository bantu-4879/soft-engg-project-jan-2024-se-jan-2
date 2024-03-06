<template>
  <div>
    <UserNavbar :id_="1"></UserNavbar>

    <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="7" md="8">
          <h3 style="text-align: center">Unresolved Tickets</h3>
          <div style="height: 550px; overflow: auto; padding: 10px">
            <SearchTicket
              :upvote_disabled="true"
              :delete_disabled="true"
              :edit_disabled="false"
            ></SearchTicket>
          </div>
        </b-col>
        <b-col cols="12" sm="5" md="4" style="border-left: dashed black">
          <h3 style="text-align: center">My Activity</h3>
          <InfoCard title="tickets resolved" :value="n_tickets_resolved.toString()"></InfoCard>
          <InfoCard
            title="tickets pending"
            :value="n_total_unresolved_tickets.toString()"
          ></InfoCard>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import InfoCard from "../components/InfoCard.vue";
import SearchTicket from "../components/SearchTicket.vue";

export default {
  name: "SupportHome",
  components: { UserNavbar, InfoCard, SearchTicket },
  data() {
    return {
      n_tickets_resolved: 0,
      n_total_unresolved_tickets: 0,

      user_id: this.$store.getters.get_user_id,
    };
  },
  created() {
    fetch(common.SUPPORT_API + `/${this.user_id}`, {
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
            message: "User data retrieved.",
          });

          this.n_tickets_resolved = data.message.n_tickets_resolved;
          this.n_total_unresolved_tickets = data.message.n_total_unresolved_tickets;
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
