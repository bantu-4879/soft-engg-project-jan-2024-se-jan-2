<template>
  <div>
    <UserNavbar :id_="1"></UserNavbar>
    <b-container fluid="xl">
      <h3 style="text-align: center">All Tickets</h3>
      <SearchTicket
        :upvote_disabled="true"
        :delete_disabled="false"
        :edit_disabled="true"
      ></SearchTicket>
    </b-container>

    <br />
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import InfoCard from "../components/InfoCard.vue";
import TicketCard from "../components/TicketCard.vue";
import SearchTicket from "../components/SearchTicket.vue";

export default {
  name: "AllTickets",
  components: { UserNavbar, InfoCard, TicketCard, SearchTicket },
  data() {
    return {
      user_id: this.$store.getters.get_user_id,
      ticket_card_details: [],
    };
  },
  created() {
    let form = {
      filter_status: ["pending"],
    };
    let params = "";
    params = new URLSearchParams(form).toString();

    fetch(common.TICKET_API_ALLTICKETS, {
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
            message: "User data retrieved.",
          });
          this.ticket_card_details = data.message;
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
