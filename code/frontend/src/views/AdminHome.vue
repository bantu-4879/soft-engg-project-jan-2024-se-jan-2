<template>
  <div>
    <UserNavbar :id_="1"></UserNavbar>
    <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="5" md="4">
          <InfoCard
            title="New Users Registered"
            :value="new_users_registered.toString()"
          ></InfoCard>
          <InfoCard
            title="Total Open Tickets"
            :value="total_open_tickets.toString()"
          ></InfoCard>
          <InfoCard
            title="Total Resolved Tickets"
            :value="total_resolved_tickets.toString()"
          ></InfoCard>
        </b-col>
        <b-col cols="12" sm="5" md="4">
          <InfoCard
            title="New Tickets Raised Today"
            :value="tickets_raised_today.toString()"
          ></InfoCard>
          <InfoCard
            title="New Tickets Raised This Week"
            :value="tickets_raised_week.toString()"
          ></InfoCard>
          <InfoCard
            title="New Tickets Raised This Month"
            :value="tickets_raised_month.toString()"
          ></InfoCard>
        </b-col>
        <b-col cols="12" sm="5" md="4">
          <InfoCard
            title="Total Student"
            :value="total_students.toString()"
          ></InfoCard>
          <InfoCard
            title="Total Support Staff"
            :value="total_support_staff.toString()"
          ></InfoCard>
          <InfoCard
            title="Total Admin"
            :value="total_admin.toString()"
          ></InfoCard>
        </b-col>
      </b-row>
    </b-container>

    <br />
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import InfoCard from "../components/InfoCard.vue";

export default {
  name: "AdminHome",
  components: { UserNavbar, InfoCard },
  data() {
    return {
      user_id: this.$store.getters.get_user_id,
      new_users_registered: 0,
      total_open_tickets: 0,
      total_resolved_tickets: 0,
      tickets_raised_today: 0,
      tickets_raised_month: 0,
      tickets_raised_week: 0,
      total_admin: 0,
      total_support_staff: 0,
      total_students: 0,
    };
  },
  created() {
    let form = {
      filter_status: ["pending"],
    };
    let params = "";
    params = new URLSearchParams(form).toString();

    fetch(common.STATS_API + '/', {
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
          this.new_users_registered = data.message.new_users_registered;
          this.total_open_tickets = data.message.total_open_tickets;
          this.total_resolved_tickets = data.message.total_resolved_tickets;
          this.tickets_raised_today = data.message.tickets_raised_today;
          this.tickets_raised_month = data.message.tickets_raised_month;
          this.tickets_raised_week = data.message.tickets_raised_week;
          this.total_admin = data.message.total_admin;
          this.total_support_staff = data.message.total_support_staff;
          this.total_students = data.message.total_students;
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
