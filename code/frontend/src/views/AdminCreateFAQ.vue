<template>
  <div>
    <UserNavbar :id_="3"></UserNavbar>
    <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="6" md="6" style="border-right: dashed black">
          <h3 style="text-align: center">Create FAQ</h3>
          <FAQForm></FAQForm>
        </b-col>
        <b-col cols="12" sm="6" md="6">
          <h3 style="text-align: center">Most Upvoted Tickets</h3>
          <SearchTicket
            :upvote_disabled="true"
            :delete_disabled="true"
            :edit_disabled="true"
          ></SearchTicket>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import TicketForm from "../components/TicketForm.vue";
import SearchTicket from "../components/SearchTicket.vue";
import FAQForm from "../components/FAQForm.vue";

export default {
  name: "AdminCreateFAQ",
  components: { UserNavbar, FAQForm, SearchTicket },
  data() {
    return {};
  },
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style></style>
