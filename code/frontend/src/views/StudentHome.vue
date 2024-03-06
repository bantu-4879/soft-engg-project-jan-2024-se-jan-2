<template>
  <div>
    <UserNavbar :id_="1"></UserNavbar>

    <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="7" md="8">
          <h3 style="text-align: center">My Unresolved Tickets</h3>
          <div style="height: 550px; overflow: auto; padding: 10px">
            <div v-for="ticket in ticket_card_details" :key="ticket.ticket_id">
              <TicketCard
                :ticket_id="ticket.ticket_id"
                :created_on="ticket.created_on"
                :title="ticket.title"
                :description="ticket.description"
                :votes="ticket.votes"
                :created_by="ticket.created_by"
                :upvote_disabled="true"
                :delete_disabled="false"
                :edit_disabled="false"
                :is_resolved="false"
              ></TicketCard>
            </div>
          </div>
        </b-col>
        <b-col cols="12" sm="5" md="4" style="border-left: dashed black">
          <h3 style="text-align: center">My Activity</h3>
          <InfoCard title="tickets created" :value="n_tickets_created.toString()"></InfoCard>
          <InfoCard title="tickets resolved" :value="n_tickets_resolved.toString()"></InfoCard>
          <InfoCard title="tickets pending" :value="n_tickets_pending.toString()"></InfoCard>
          <InfoCard title="tickets upvoted" :value="n_tickets_upvoted.toString()"></InfoCard>
        </b-col>
      </b-row>
    </b-container>

    <br />
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import TicketCard from "../components/TicketCard.vue";
import InfoCard from "../components/InfoCard.vue";

export default {
  name: "StudentHome",
  components: { UserNavbar, TicketCard, InfoCard },
  data() {
    return {
      n_tickets_created: 0,
      n_tickets_resolved: 0,
      n_tickets_pending: 0,
      n_tickets_upvoted: 0,
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

    fetch(common.STUDENT_API + `/${this.user_id}`, {
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
          this.n_tickets_created = data.message.n_tickets_created;
          this.n_tickets_resolved = data.message.n_tickets_resolved;
          this.n_tickets_pending = data.message.n_tickets_pending;
          this.n_tickets_upvoted = data.message.n_tickets_upvoted;
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

    fetch(common.TICKET_API_ALLTICKETS + `/${this.user_id}` + "?" + params, {
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
            message: `Total ${data.message.length} Tickets retrieved.`,
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
