<template>
    <div>
      <UserNavbar :id_="2"></UserNavbar>
  
      <b-container fluid="xl">
        <b-row class="text-start">
          <b-col cols="12" sm="6" md="12" style="border-right: dashed black">
            <h3 style="text-align: center">Create Discourse Ticket</h3>
            <DiscourseTicketCard v-if="showDiscourseTicketForm"></DiscourseTicketCard>
          </b-col>
        </b-row>
      </b-container>
  
      <br />
    </div>
  </template>
  
  <script>
  import UserNavbar from "../components/UserNavbar.vue";
  import DiscourseTicketCard from "../components/DiscourseTopicCardForm.vue";
  import SearchTicket from "../components/SearchTicket.vue";
  
  export default {
    name: "StudentCreateDiscourseTopic",
    components: { UserNavbar, DiscourseTicketCard, SearchTicket },
    data() {
      return {
        showDiscourseTicketForm:false,
      };
    },
    mounted() {},
    methods: {},
    computed: {},
  };
  </script>
  
  <style></style>
  