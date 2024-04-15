<template>
  <div>
    <UserNavbar :id_="2"></UserNavbar>

    <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="6" md="5" style="border-right: dashed black">
          <h3 style="text-align: center">Create Ticket</h3>
          <TicketForm :hideReset=false :editTicket=false></TicketForm>
        </b-col>
        <b-col cols="12" sm="6" md="7">
          <h3 style="text-align: center">Search Tickets</h3>
          <SearchTicket :upvote_disabled="false"
          :delete_disabled="true"
          :edit_disabled="true"></SearchTicket>
        </b-col>
      </b-row>
    </b-container>

    <br />
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import TicketForm from "../components/TicketForm.vue";
import SearchTicket from "../components/SearchTicket.vue";
import DiscourseTicketCard from "../components/DiscourseTopicCardForm.vue";

export default {
  name: "StudentCreateTicket",
  components: { UserNavbar, TicketForm, SearchTicket,DiscourseTicketCard },
  data() {
    return {
      showDiscourseTicketForm:false,
      ticketId:'',
    };
  },
  mounted() {},
  methods: {
    handleTicketCreated(ticketId) {
      this.ticketId=ticketId;
      console.log(ticketId);
      console.log(this.ticketId);
      this.showDiscourseTicketForm = true;
    },
    handleDisccourseCreated()
    {
      this.showDiscourseTicketForm=false;
    }
  },
  computed: {},
};
</script>

<style></style>
