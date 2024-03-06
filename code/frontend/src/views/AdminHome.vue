<template>
  <div>
    <UserNavbar :id_="1"></UserNavbar>
    <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="5" md="4">
          <InfoCard
            title="New User Registered"
            :value="new_registered_users().toString()"
          ></InfoCard>
          <InfoCard
            title="Total Open Tickets"
            :value="n_total_unresolved_tickets.toString()"
          ></InfoCard>
          <InfoCard
            title="Total Resolved Tickets"
            :value="n_total_resolved_tickets.toString()"
          ></InfoCard>
        </b-col>
        <b-col cols="12" sm="5" md="4">
          <InfoCard title="New Tickets Raised Today" :value="n_tickets_today.toString()"></InfoCard>
          <InfoCard
            title="New Tickets Raised This Week"
            :value="n_tickets_week.toString()"
          ></InfoCard>
          <InfoCard
            title="New Tickets Raised This Month"
            :value="n_tickets_month.toString()"
          ></InfoCard>
        </b-col>
        <b-col cols="12" sm="5" md="4">
          <InfoCard title="Total Student" :value="n_student.toString()"></InfoCard>
          <InfoCard title="Total Support Staff" :value="n_support.toString()"></InfoCard>
          <InfoCard title="Total Admin" :value="n_admin.toString()"></InfoCard>
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
      n_total_unresolved_tickets: 0,
      n_total_resolved_tickets: 0,
      n_tickets_today: 0,
      n_tickets_week: 0,
      n_tickets_month: 0,
      n_student: 0,
      n_support: 0,
      n_admin: 0,
      n_student_new: 0,
      n_support_new: 0,
      n_user_new: 0,
    };
  },
  created() {
    let form = {
      filter_status: ["pending"],
    };
    let params = "";
    params = new URLSearchParams(form).toString();

    fetch(common.ADMIN_API + `/${this.user_id}`, {
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
          this.n_total_unresolved_tickets = data.message.n_total_unresolved_tickets;
          this.n_total_resolved_tickets = data.message.n_total_resolved_tickets;
          this.n_tickets_today = data.message.n_tickets_today;
          this.n_tickets_week = data.message.n_tickets_week;
          this.n_tickets_month = data.message.n_tickets_month;
          this.n_student = data.message.n_student;
          this.n_support = data.message.n_support;
          this.n_admin = data.message.n_admin;
          this.n_student_new = data.message.n_student_new;
          this.n_support_new = data.message.n_support_new;
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

    this.n_user_new = this.n_student_new + this.n_support_new;
  },
  mounted() {},
  methods: {
    new_registered_users: function () {
      this.n_user_new = this.n_student_new + this.n_support_new;
      return this.n_user_new;
    },
  },
  computed: {},
};
</script>

<style></style>
