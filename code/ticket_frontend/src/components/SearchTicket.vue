<template>
  <div
    class="search-ticket-form"
    style="margin-top: 5px; margin-left: 5px; margin-right: 5px; text-align: left"
  >
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-container class="search-filters" style="margin: 5px; padding: 5px">
        <b-row class="row">
          <b-col class="col" cols="12" md="6" sm="12">
            <b-form-group>
              <label for="input-query">Search Query:</label>
              <b-form-input
                id="input-query"
                v-model="form.query"
                type="text"
                placeholder="Enter search query"
                :state="check_query"
                aria-describedby="input-live-feedback-query"
              ></b-form-input>
            </b-form-group>
          </b-col>
          <b-col class="col" cols="12" md="3" sm="6">
            <b-form-group id="input-sort" label="Sort By: " label-for="input-sort">
              <b-form-select
                id="input-sort"
                v-model="form.sortby"
                :options="sort_by_options"
              ></b-form-select>
            </b-form-group>
          </b-col>
          <b-col class="col" cols="12" md="3" sm="6">
            <b-form-group id="input-sort-dir" label="Sort Direction: " label-for="input-sort-dir">
              <b-form-select
                id="input-sort-dir"
                v-model="form.sortdir"
                :options="sort_dir_options"
              ></b-form-select>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row class="row">
          <b-col class="col" cols="12" md="6" sm="12"
            ><Tagging @tags_changed="onTagsChanged"></Tagging
          ></b-col>
          <b-col class="col" cols="12" md="3" sm="6">
            <b-form-group label="Filter Priority:">
              <b-form-checkbox-group
                v-model="form.filter_priority"
                :options="filter_priority_options"
                value-field="item"
                text-field="name"
              ></b-form-checkbox-group
            ></b-form-group>
          </b-col>
          <b-col class="col" cols="12" md="3" sm="6">
            <b-form-group label="Filter Status:">
              <b-form-checkbox-group
                v-model="form.filter_status"
                :options="filter_status_options"
                value-field="item"
                text-field="name"
                disabled-field="disabled"
              ></b-form-checkbox-group
            ></b-form-group>
          </b-col>
        </b-row>
      </b-container>
      <b-button style="margin: 10px" type="submit" variant="primary">Submit</b-button>
      <b-button style="margin: 10px" type="reset" variant="danger">Reset</b-button>
    </b-form>
    <br />

    <h3 style="text-align: center">Results</h3>
    <div style="height: 500px; overflow: auto; padding: 10px">
      <div v-for="ticket in ticket_card_details" :key="ticket.ticket_id">
        <TicketCard
          :ticket_id="ticket.ticket_id"
          :created_on="ticket.created_on"
          :title="ticket.title"
          :description="ticket.description"
          :votes="ticket.votes"
          :created_by="ticket.created_by"
          :upvote_disabled="upvote_disabled"
          :delete_disabled="delete_disabled"
          :edit_disabled="edit_disabled"
          :is_resolved="ticket.status == 'resolved'"
        ></TicketCard>
      </div>
    </div>
  </div>
</template>

<script>
import * as common from "../assets/common.js";
import Tagging from "./Tagging.vue";
import TicketCard from "../components/TicketCard.vue";

export default {
  name: "SearchTicket",
  components: { Tagging, TicketCard },
  props: ["upvote_disabled", "delete_disabled", "edit_disabled"],
  data() {
    return {
      filter_priority_options: [
        { item: "low", name: "Low" },
        { item: "medium", name: "Medium" },
        { item: "high", name: "High" },
      ],
      filter_status_options: [
        { item: "pending", name: "Pending", disabled: false },
        { item: "resolved", name: "Resolved", disabled: false },
      ],

      sort_by_options: [
        { value: "created_on", text: "Created Date" },
        { value: "resolved_on", text: "Resolved Date" },
        { value: "votes", text: "Votes" },
      ],
      sort_dir_options: [
        { value: "asc", text: "Ascending" },
        { value: "desc", text: "Descending" },
      ],
      form: {
        query: "",
        filter_priority: [],
        filter_status: [],
        sortby: "",
        sortdir: "",
        filter_tags: [],
      },
      show: true,
      ticket_card_details: [],
      user_role: this.$store.getters.get_user_role,
      current_page_path: this.$route.path,
      user_id: this.$store.getters.get_user_id,
      search_url: common.TICKET_API_ALLTICKETS,
    };
  },
  created() {
    // here update filter sort options as per user and page

    if (this.user_role === "student" && this.current_page_path === "/student-create-ticket") {
      // all options will be available and all users tickets checked
      this.form.sortdir = "desc";
      this.form.sortby = "votes";
    }
    if (this.user_role === "student" && this.current_page_path === "/student-my-tickets") {
      // all options will be available and only current student tickets checked

      this.search_url = this.search_url + `/${this.user_id}`;
    }
    if (this.user_role === "support" && this.current_page_path === "/support-home") {
      // show all unresolved tickets, status=pending, filter on priority and tags, sort by created date and votes.

      this.filter_status_options = this.filter_status_options.filter(
        (value) => value.item == "pending"
      );
      this.form.filter_status.push("pending");
      this.search_url = this.search_url + `/${this.user_id}`;
    }
    if (this.user_role === "support" && this.current_page_path === "/support-my-tickets") {
      // show user's resolved tickets, status=resolved, filter on priority and tags, sort by created date, resolved date and votes.

      this.filter_status_options = this.filter_status_options.filter(
        (value) => value.item == "resolved"
      );
      this.form.filter_status.push("resolved");
      this.search_url = this.search_url + `/${this.user_id}`;
    }
    if (this.user_role === "admin" && this.current_page_path === "/admin-create-faq") {
      // show all resolved tickets, status=resolved, filter on priority and tags, sort by created date, resolved date and votes.

      this.filter_status_options = this.filter_status_options.filter(
        (value) => value.item == "resolved"
      );
      this.form.filter_status.push("resolved");
      this.form.sortdir = "desc";
      this.sort_by_options = this.sort_by_options.filter((value) => value.value == "votes");
      this.search_url = this.search_url + `/${this.user_id}`;
      this.form.sortby = "votes";
    }
    this.onSubmit();
  },
  methods: {
    onSubmit(event) {
      if (event && event.preventDefault) {
        event.preventDefault();
      }
      // convert form to query params
      let params = "";
      params = new URLSearchParams(this.form).toString();

      fetch(this.search_url + "?" + params, {
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
    onReset(event) {
      if (event && event.preventDefault) {
        event.preventDefault();
      }
      this.form.query = "";
      this.form.sortby = "";
      this.form.sortdir = "";
      this.form.filter_status = [];

      if (this.user_role === "support" && this.current_page_path === "/support-home") {
        this.filter_status_options = this.filter_status_options.filter(
          (value) => value.item == "pending"
        );
        this.form.filter_status.push("pending");
      }
      if (this.user_role === "support" && this.current_page_path === "/support-my-tickets") {
        this.filter_status_options = this.filter_status_options.filter(
          (value) => value.item == "resolved"
        );
        this.form.filter_status.push("resolved");
      }
      if (this.user_role === "admin" && this.current_page_path === "/admin-create-faq") {
        this.filter_status_options = this.filter_status_options.filter(
          (value) => value.item == "resolved"
        );
        this.form.filter_status.push("resolved");
        this.form.sortdir = "desc";
        this.sort_by_options = this.sort_by_options.filter((value) => value.value == "votes");
        this.form.sortby = "votes";
      }

      this.form.filter_priority = [];
      this.ticket_card_details = [];
      this.show = false;
      this.onSubmit();
      this.$nextTick(() => {
        this.show = true;
      });
    },
    onTagsChanged(value) {
      this.form.filter_tags = value;
    },
  },
  computed: {
    check_query() {
      // not being used in dev stage
      return this.form.query.length > 0 ? true : true;
    },
  },

  watch: {
    value: {
      ticket_card_details(newValue, oldValue) {
        // Note: this is a deep watcher
        this.$forceUpdate();
      },
      deep: true,
    },
  },
};
</script>

<style></style>
