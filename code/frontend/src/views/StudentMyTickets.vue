<template>
    <div>
      
      <UserNavbar :id_="3"></UserNavbar>
      
      <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="12" md="12">
          <SearchTicket :upvote_disabled="true"
          :delete_disabled="false"
          :edit_disabled="false" :discourse_disabled="false"></SearchTicket>
        </b-col>
      </b-row>
    </b-container>
      
    </div>
</template>

<script>
import UserNavbar from '../components/UserNavbar.vue';
import SearchTicket from "../components/SearchTicket.vue";


export default {
  name: 'StudentMyTickets',
  components: {UserNavbar, SearchTicket},
  data() {
    return {
    };
  },
  mounted() {},
  methods: {
    
  },
  computed: {},
};
</script>

<style>


</style>
