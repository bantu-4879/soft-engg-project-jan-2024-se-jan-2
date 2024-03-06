<template>
  <div
    class="ticket-form"
    style="margin-top: 5px; margin-left: 5px; margin-right: 5px; text-align: left"
  >
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        ><b-form-input
          id="input-title"
          v-model="form.title"
          type="text"
          placeholder="Enter title"
          :state="check_title"
          aria-describedby="input-live-feedback-title"
          :disabled="user_role == 'student' ? false : true"
          required
        ></b-form-input>
        <b-form-invalid-feedback id="input-live-feedback-title">
          Title should be atleast 5 characters long.
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        ><b-form-textarea
          id="input-description"
          v-model="form.description"
          type="text"
          placeholder="Enter description (Optional)"
          rows="3"
          max-rows="6"
          :disabled="user_role == 'student' ? false : true"
        ></b-form-textarea
      ></b-form-group>

      <Tagging
        @tags_changed="onTagsChanged"
        v-show="user_role == 'student' ? true : false"
      ></Tagging>

      <b-form-group
        label="Select priority:"
        v-slot="{ ariaDescribedby }"
        v-show="user_role == 'student' ? true : false"
      >
        <b-form-radio-group
          id="radio-group-priority"
          v-model="form.priority"
          :options="priority_options"
          :aria-describedby="ariaDescribedby"
          name="radio-group-priority"
        ></b-form-radio-group>
      </b-form-group>

      <b-form-group v-show="user_role == 'student' ? false : true"
        ><b-form-textarea
          id="input-solution"
          v-model="form.solution"
          type="text"
          placeholder="Enter solution"
          rows="3"
          max-rows="6"
        ></b-form-textarea
      ></b-form-group>

      <FileUpload @file_uploading="onFileUpload"></FileUpload>

      <br />
      <br />
      <b-button style="margin: 10px" type="submit" variant="primary">Submit</b-button>
      <b-button v-show="hideReset ? false : true" style="margin: 10px" type="reset" variant="danger"
        >Reset</b-button
      >
    </b-form>
    <br />
  </div>
</template>

<script>
import * as common from "../assets/common.js";
import FileUpload from "./FileUpload.vue";
import Tagging from "./Tagging.vue";

export default {
  name: "TicketForm",
  props: ["ticket_id", "title", "description", "priority", "tags", "hideReset", "editTicket"],
  components: { Tagging, FileUpload },
  data() {
    return {
      priority_options: [
        { text: "Low", value: "low" },
        { text: "Medium", value: "medium" },
        { text: "High", value: "high" },
      ],
      form: {
        title: this.title ? this.title : "",
        description: this.description ? this.description : "",
        priority: this.priority ? this.priority : "low",
        solution: "",
        tags: [],
        tag_1: "",
        tag_2: "",
        tag_3: "",
        attachments: [],
      },
      user_role: this.$store.getters.get_user_role,
      show: true,
    };
  },
  created() {},
  methods: {
    onFileUpload(value) {
      this.form.attachments.splice(0, this.form.attachments.length, ...value);
      for (let i = 0; i < this.form.attachments.length; i++) {}
    },
    onSubmit(event) {
      if (event && event.preventDefault) {
        event.preventDefault();
      }

      if (this.user_role == "student" && this.form.tags.length == 0 && this.check_title) {
        alert("Choose atleast 1 tag and title should be atleast 5 characters long.");
      } else {
        alert('Submitting form. Click "Ok" to proceed?');
        this.$log.info("Submitting Ticket form");

        for (let i in this.form.tags) {
          if (this.form.tags[i]) {
            this.form[`tag_${parseInt(i) + 1}`] = this.form.tags[i];
          }
        }

        let fetch_url = "";
        let method = "";
        if (this.editTicket) {
          fetch_url =
            common.TICKET_API + `/${this.ticket_id}` + `/${this.$store.getters.get_user_id}`;
          method = "PUT";
        } else {
          fetch_url = common.TICKET_API + `/${this.$store.getters.get_user_id}`;
          method = "POST";
        }

        fetch(fetch_url, {
          method: method,
          headers: {
            "Content-Type": "application/json",
            web_token: this.$store.getters.get_web_token,
            user_id: this.$store.getters.get_user_id,
          },
          body: JSON.stringify(this.form),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.category == "success") {
              this.flashMessage.success({
                message: data.message,
              });
              if (!this.editTicket) {
                this.onReset();
              }
              if (this.user_role == "support") {
                this.$emit("ticketResolved");
              }
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
      }
    },
    onReset(event) {
      if (event && event.preventDefault) {
        event.preventDefault();
      }
      this.form.title = "";
      this.form.description = "";
      this.solution = "";
      this.form.attachments = [];
      this.form.tags = [];
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    onTagsChanged(value) {
      this.form.tags = value;
    },
  },
  computed: {
    check_title() {
      return this.form.title.length > 5 ? true : false;
    },
  },
};
</script>

<style></style>
