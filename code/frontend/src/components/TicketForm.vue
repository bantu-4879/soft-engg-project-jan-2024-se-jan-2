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
  props: ["id", "title", "description", "priority", "tags", "hideReset", "editTicket"],
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
        tags_list: [],
        attachments: [],
      },
      user_role: this.$store.getters.get_user_role,
      show: true,
      ticket_id:null,
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

      if (this.form.tags_list.length == 0 && this.check_title =="") {
        alert("Choose atleast 1 tag and title should be atleast 5 characters long.");
      } else {
        alert('Submitting form. Click "Ok" to proceed?');
        this.$log.info("Submitting Ticket form");

        let fetch_url = "";
        let method = "";
        if (this.editTicket) {
          fetch_url =
            common.TICKET_API + `/${this.id}` + `/${this.$store.getters.get_user_id}`;
          method = "PUT";
        } else {
          fetch_url = common.TICKET_API + `/${this.$store.getters.get_user_id}`;
          method = "POST";
        }

        fetch(fetch_url, {
          method: method,
          headers: {
            "Content-Type": "application/json",
            webtoken: this.$store.getters.get_web_token,
            userid: this.$store.getters.get_user_id,
          },
          body: JSON.stringify(this.form),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.category === "success") {
              const ticketId = data.ticket_id;
              console.log(ticketId)
              this.ticket_id=data.ticket_id;
              console.log(this.ticket_id);
              this.flashMessage.success({
                message: data.message,
              });
              if (!this.editTicket) {
                this.onReset();
              }
              if (this.user_role == "staff") {
                
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

      if(this.form.priority == "high" && this.user_role == "student") {
        let webhook_url = common.WEBHOOK_URL_STAFF;
        let webhook_message = {
          "cards": [
            {
              "header": {
                "title": "High Priority Ticket",
                "subtitle": "Title: " + this.form.title,
                "imageUrl": "https://workable-application-form.s3.amazonaws.com/advanced/production/61557f91d9510741dc62e7f8/c3635b59-a3d2-444a-b636-a9d0061dcdde", // Optional: You can include an image URL here
              },
              "sections": [
                {
                  "widgets": [
                    {
                      "keyValue": {
                        "topLabel": "Created By",
                        "content": this.$store.getters.get_user_name,
                        "contentMultiline": false
                      }
                    }
                  ]
                },
                {
                  "widgets": [
                    {
                      "textParagraph": {
                        "text": "Description: " + this.form.description
                      }
                    }
                  ]
                }
              ]
            }
          ]
        };

        fetch(webhook_url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json; charset=UTF-8", 
          },
          body: JSON.stringify(webhook_message),
        })
          .then((response) => response.json())
          .then((data) => {
            this.flashMessage.success({
                message: "Notified support team staff about high priority ticket.",
              });
          })
        
      }

      if(this.user_role == "staff") {
        let webhook_url = common.WEBHOOK_URL_STUDENT;
        let webhook_message = {
          "cards": [
            {
              "header": {
                "title": "Ticket Update",
                "subtitle": "Title: " + this.form.title,
                "imageUrl": "https://static.wikia.nocookie.net/gamia_gamepedia_en/images/a/ab/Icon-Oggy-and-the-Cockroaches-EU-iOS.png/revision/latest?cb=20180806161726", // Optional: You can include an image URL here
              },
              "sections": [
                {
                  "widgets": [
                    {
                      "keyValue": {
                        "topLabel": "Resolved By",
                        "content": this.$store.getters.get_user_name,
                        "contentMultiline": false
                      }
                    }
                  ]
                },
                {
                  "widgets": [
                    {
                      "textParagraph": {
                        "text": "Solution: " + this.form.solution
                      }
                    }
                  ]
                }
              ]
            }
          ]
        };

        fetch(webhook_url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json; charset=UTF-8", 
          },
          body: JSON.stringify(webhook_message),
        })
          .then((response) => response.json())
          .then((data) => {
            this.flashMessage.success({
                message: "Notified student about ticket update.",
              });
          })
        
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
      this.form.tags_list = [];
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    onTagsChanged(value) {
      this.form.tags_list = value;
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
