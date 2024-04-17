<template>
    <div>
      <UserNavbar :id_="2"></UserNavbar>
  
      <b-container fluid="xl">
        <b-row class="text-start">
          <b-col cols="12" sm="6" md="12" style="border-right: dashed black">
            <h3 style="text-align: center">Create Discourse Ticket</h3>
            <DiscourseTopicCardForm :ticketId="ticket_id"></DiscourseTopicCardForm>
          </b-col>
        </b-row>
      </b-container>
  
      <br />
    </div>
  </template>
  
  <script>
  import UserNavbar from "../components/UserNavbar.vue";
  import DiscourseTopicCardForm from "../components/DiscourseTopicCardForm.vue";
  import SearchTicket from "../components/SearchTicket.vue";
  
  export default {
    name: "StudentCreateDiscourseTopic",
    components: { UserNavbar, DiscourseTopicCardForm, SearchTicket },
    data() {
      return {
        ticket_id:null
      };
    },
    created()
    {
      this.ticket_id = this.$route.params.ticketId
    },
    mounted() {

    },
    methods: {},
    computed: {},
  };
  </script>
  
  <style></style>
  