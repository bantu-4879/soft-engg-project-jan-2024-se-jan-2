<template>
  <div>
    <template v-if="id">
      <b-container
        class="ticket-card-container"
        v-show="!ticket_deleted"
        :style="[
          user_id == user_id && $route.path == '/student-create-ticket'
            ? { 'background-color': 'rgb(225, 245, 250)' }
            : { 'background-color': 'rgb(251, 252, 252)' },
        ]"
      >
        <!-- Stack the columns on mobile by making one full-width and the other half-width -->
        <b-row class="row" @click="getTicketDetails">
          <b-col class="col" cols="12" lg="5" sm="12"
            ><i>Id: </i>{{ id.slice(0, 15) }}</b-col
          >
          <b-col class="col" cols="12" lg="5" sm="8"
            ><i>Created At: </i>{{ created_at }}</b-col
          >
        </b-row>
        <b-row class="row">
          <b-col
            class="col"
            cols="12"
            sm="10"
            lg="11"
            @click="getTicketDetails"
          >
            <b-row class="row">
              <b-col class="col" cols="12"
                ><b>Title: </b>{{ title.slice(0, 80) }}</b-col
              >
            </b-row>
            <b-row class="row">
              <b-col class="col" cols="12"
                ><b>Description: </b>{{ description.slice(0, 200) }}</b-col
              >
            </b-row>
          </b-col>
          <b-col class="col" cols="12" sm="2" lg="1">
            <b-row class="row">
              <b-col class="col" cols="4" sm="12" lg="12">
                <b-button
                  @click="upvoteTicket"
                  variant="outline-light"
                  size="sm"
                  class="ticket-card-buttons"
                  :disabled="upvote_disabled"
                  v-show="
                    upvote_disabled
                      ? !upvote_disabled
                      : user_id !== user_id &&
                        user_role == 'student' &&
                        !is_resolved
                  "
                  ><b-icon
                    icon="heart-fill"
                    aria-hidden="true"
                    class="bg-light"
                    variant="success"
                  ></b-icon>
                </b-button>
              </b-col>
              <b-col class="col" cols="4" sm="12" lg="12"
                ><b-button
                  @click="showDiscourse"
                  variant="outline-light"
                  size="sm"
                  class="ticket-card-buttons"
                  ><b-icon
                    icon="chat-left-quote-fill"
                    aria-hidden="true"
                    class="bg-light"
                    variant="primary"
                  ></b-icon
                ></b-button>
              </b-col>
              <b-col class="col" cols="4" sm="12" lg="12"
                ><b-button
                  @click="showDiscourseTicketModal"
                  variant="outline-light"
                  size="sm"
                  class="ticket-card-buttons"
                  :disabled="discourse_disabled"
                  v-show="
                    discourse_disabled
                      ? !discourse_disabled
                      : user_id == user_id && !is_resolved
                  "
                  ><b-icon
                    icon="chat-dots-fill"
                    aria-hidden="true"
                    class="bg-light"
                    variant="primary"
                  ></b-icon
                ></b-button>
              </b-col>

              <b-col class="col" cols="4" sm="12" lg="12"
                ><b-button
                  @click="showEditTicketModal"
                  variant="outline-light"
                  size="sm"
                  class="ticket-card-buttons"
                  :disabled="edit_disabled"
                  v-show="
                    edit_disabled
                      ? !edit_disabled
                      : (user_id == user_id || user_role == 'staff') &&
                        !is_resolved
                  "
                  ><b-icon
                    icon="pencil-fill"
                    aria-hidden="true"
                    class="bg-light"
                    variant="primary"
                  ></b-icon
                ></b-button>
              </b-col>

              <b-col class="col" cols="4" sm="12" lg="12"
                ><b-button
                  @click="showDeleteTicketModal"
                  variant="outline-light"
                  size="sm"
                  class="ticket-card-buttons"
                  :disabled="delete_disabled"
                  v-show="
                    delete_disabled ? !delete_disabled : user_id == user_id
                  "
                  ><b-icon
                    icon="trash-fill"
                    aria-hidden="true"
                    class="bg-light"
                    variant="danger"
                  ></b-icon></b-button
              ></b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-container>
    </template>

    <b-modal
      :id="show_ticket_modal_id"
      @cancel="$bvModal.hide(show_ticket_modal_id)"
      size="xl"
      scrollable
    >
      <template #modal-header="{ cancel }">
        <span style="font-size: 20px">Ticket ID: {{ id }}</span>
        <b-button size="sm" variant="outline-danger" @click="cancel()">
          Close
        </b-button>
      </template>

      <div class="d-block text-left">
        <h5 style="text-align: center">{{ title }}</h5>

        <!-- Three parallel divisions with separate borders -->
        <div class="ticket-indicator">
          <div class="dark-bg border-item">
            <p>Status: {{ ticket_status }}</p>
          </div>
          <div class="dark-bg border-item">
            <p>Priority: {{ ticket_priority }}</p>
          </div>
          <div class="dark-bg border-item">
            <p>
              Tags: <span class="light-bg">{{ tags_list }}</span>
            </p>
          </div>
        </div>

        <!-- Description section -->
        <div class="ticket-section">
          <h6>Description:</h6>
          <p>{{ description }}</p>
        </div>

        <!-- Three parallel sections -->
        <div class="ticket-indicator">
          <div class="border-item">
            <p>
              <span class="dark-bg">Created by:</span>
              {{ created_by_full_name }}
            </p>
          </div>
          <div class="border-item">
            <p>
              <span class="dark-bg">Created on:</span>
              {{ Date(created_at).toLocaleString() }}
            </p>
          </div>
          <div class="border-item" v-if="resolved_by">
            <p>
              <span class="dark-bg">Resolved by:</span>
              {{ resolved_by_full_name }}
            </p>
          </div>
        </div>

        <!-- Solution and Attachments -->
        <div class="ticket-section" :class="{ 'green-bg': resolved_by != 0 }">
          <h6>Solution:</h6>
          <p>{{ solution }}</p>
        </div>

        <div class="ticket-section">
          <h6>Attachments:</h6>
          <div v-for="(attach, imageIndex) in attachments" :key="imageIndex">
            <img :src="attach.attachment_loc" class="img-fluid" />
          </div>
        </div>
      </div>
      <div class="ticket-section" v-show="showComments">
        <h6>Comments</h6>
        <div v-for="comment in comments" :key="comment.id">
          <p class="badge badge-info">
            <i>{{ comment.commenter }} </i><br />
            <i> {{ comment.added_at }}</i>
            <br /><br />{{ comment.comment }}
          </p>
        </div>
        <b-form @submit.prevent="addComment">
          <b-row>
            <b-col sm="10">
              <b-form-textarea
                id="textarea-small"
                size="sm"
                placeholder="Add Comment"
                v-model="comment_input"
              ></b-form-textarea>
            </b-col>
            <b-col>
              <b-button type="submit" variant="light"> Add Comment</b-button>
            </b-col>
          </b-row>
        </b-form>
      </div>
      <!-- <div class="ticket-section">
        <h6>Tracking Data</h6>
        <div v-for="data in tracking_data" :key="data.id">
          {{ data }}
        </div>
      </div> -->
      <b-form @submit.prevent="escalateTicket">
        <b-button
          type="submit"
          variant="primary"
          v-show="!showComments"
          :diabled="already_escalated"
        >
          Escalate Ticket
        </b-button>
      </b-form>

      <template #modal-footer="{ cancel }">
        <b-button size="sm" variant="danger" @click="cancel()">
          Cancel
        </b-button>
      </template>
    </b-modal>

    <b-modal
      :id="delete_ticket_modal_id"
      @cancel="$bvModal.hide(delete_ticket_modal_id)"
      @ok="deleteTicket()"
      size="sm"
      scrollable
    >
      <template #modal-header="{ cancel }">
        <span style="font-size: 20px">Delete Ticket ?</span>
        <b-button size="sm" variant="outline-danger" @click="cancel()">
          Close
        </b-button>
      </template>

      <template #modal-footer="{ ok, cancel }">
        <b-button size="sm" variant="secondary" @click="cancel()">
          Cancel
        </b-button>
        <b-button size="sm" variant="danger" @click="ok()"> Ok </b-button>
      </template>
    </b-modal>

    <b-modal
      :id="edit_ticket_modal_id"
      @cancel="$bvModal.hide(edit_ticket_modal_id)"
      size="xl"
      scrollable
    >
      <template #modal-header="{ cancel }">
        <span style="font-size: 20px">Ticket ID: {{ id }}</span>
        <b-button size="sm" variant="outline-danger" @click="cancel()">
          Close
        </b-button>
      </template>

      <div class="d-block text-left">
        <h5 style="text-align: center">Edit Ticket Details</h5>
        <!-- display as a table -->
        <TicketForm
          :id="id"
          :title="title"
          :description="description"
          :ticket_priority="ticket_priority"
          :tags_list="tags_list"
          :hideReset="true"
          :editTicket="true"
          @ticketResolved="ticketResolvedFn"
        ></TicketForm>
      </div>

      <template #modal-footer="{ cancel }">
        <b-button size="sm" variant="secondary" @click="cancel()">
          Cancel
        </b-button>
      </template>
    </b-modal>

    <b-modal
      :id="discourse_ticket_modal_id"
      @cancel="$bvModal.hide(discourse_ticket_modal_id)"
      size="xl"
      scrollable
    >
      <template #modal-header="{ cancel }">
        <span style="font-size: 20px">Ticket ID: {{ id }}</span>
        <b-button size="sm" variant="outline-danger" @click="cancel()">
          Close
        </b-button>
      </template>

      <div class="d-block text-left">
        <h5 style="text-align: center">Discourse Topic Creation Form</h5>
        <!-- display as a table -->
        <DiscourseTicketForm
          :id="id"
          :title="title"
          :description="description"
          @DiscourseTopicCreated="$bvModal.hide(discourse_ticket_modal_id)"
        ></DiscourseTicketForm>
      </div>

      <template #modal-footer="{ cancel }">
        <b-button size="sm" variant="secondary" @click="cancel()">
          Cancel
        </b-button>
      </template>
    </b-modal>

    <b-modal
      :id="discourse_show_modal_id"
      @cancel="$bvModal.hide(discourse_show_modal_id)"
      size="xl"
      scrollable
    >
      <template #modal-header="{ cancel }">
        <span style="font-size: 20px">Ticket ID: {{ id }}</span>
        <b-button size="sm" variant="outline-danger" @click="cancel()">
          Close
        </b-button>
      </template>

      <div class="d-block text-left">
        <h5 style="text-align: center">Discourse Thread</h5>
        <Discourse :id="id"></Discourse>
      </div>
    </b-modal>
  </div>
</template>

<script>
import * as common from "../assets/common.js";
import TicketForm from "../components/TicketForm.vue";
import DiscourseTicketForm from "../components/DiscoursePopUp.vue";
import Discourse from "../components/Discourse.vue";

export default {
  name: "TicketCard",
  props: [
    "id",
    "created_at",
    "title",
    "description",
    "user_id",
    "upvote_disabled",
    "delete_disabled",
    "edit_disabled",
    "discourse_disabled",
    "is_resolved",
  ],
  components: { TicketForm, DiscourseTicketForm, Discourse },
  data() {
    return {
      button_1_active: false,
      user_id: this.$store.getters.get_user_id,
      user_role: this.$store.getters.get_user_role,
      show_ticket_modal_id: "show_ticket_modal_" + this.id,
      edit_ticket_modal_id: "edit_ticket_modal_" + this.id,
      delete_ticket_modal_id: "delete_ticket_modal_" + this.id,
      discourse_ticket_modal_id: "discourse_ticket_modal_" + this.id,
      discourse_show_modal_id: "discourse_show_modal_" + this.id,
      ticket_priority: "",
      ticket_status: "",
      solution: "",
      resolved_by: 0,
      tags_list: "",
      attachments: [],
      ticket_deleted: false,
      created_by: 0,
      created_by_full_name: "",
      resolved_by_full_name: "Not Resolved",
      comments: [],
      comment_input: "",
      show_comments: false,
      already_escalated: false,
    };
  },
  created() {},
  mounted() {
    this.userdetails();
    this.getComments();
    this.commentsVisible();
    this.getTrackingData(); 
  },
  methods: {
    ticketResolvedFn() {
      this.ticket_deleted = true; // its not deletd, its resolved , so its hidden
    },
    getTicketDetails() {
      fetch(common.TICKET_API + `/${this.id}` + `/${this.user_id}`, {
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
            // load data
            this.title = data.message.title;
            this.description = data.message.description;
            this.created_by = data.message.user_id;
            this.ticket_priority = data.message.ticket_priority;
            this.ticket_status = data.message.ticket_status;
            this.solution = data.message.solution;
            this.resolved_by = data.message.resolved_by;
            // this.resolved_on = data.message.resolved_on;
            this.tags_list = data.message.tags_list;
            this.attachments = data.message.attachments;

            // Call userdetails method after resolved_by is updated
            this.userdetails();
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

      // show modal
      this.showTicketModal();
    },
    showTicketModal() {
      this.$bvModal.show(this.show_ticket_modal_id);
    },
    showDeleteTicketModal() {
      this.$bvModal.show(this.delete_ticket_modal_id);
    },
    showEditTicketModal() {
      this.$bvModal.show(this.edit_ticket_modal_id);
    },
    showDiscourseTicketModal() {
      this.$bvModal.show(this.discourse_ticket_modal_id);
    },
    showDiscourse() {
      this.$bvModal.show(this.discourse_show_modal_id);
    },
    upvoteTicket() {
      if (this.user_id == this.user_id) {
        this.flashMessage.error({
          message: "Can't upvote own ticket.",
        });
      } else {
        fetch(common.TICKET_API + `/${this.id}` + `/${this.user_id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            webtoken: this.$store.getters.get_web_token,
            userid: this.user_id,
          },
          body: JSON.stringify({}), // empty body
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.category == "success") {
              this.flashMessage.success({
                message: data.message,
              });
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
    deleteTicket() {
      fetch(common.TICKET_API + `/${this.id}` + `/${this.user_id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          webtoken: this.$store.getters.get_web_token,
          userid: this.user_id,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.ticket_deleted = true;
            this.flashMessage.success({
              message: data.message,
            });
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
    userdetails() {
      if (this.created_by) {
        fetch(common.USERDETAILS_API + `/${this.created_by}`, {
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
              this.created_by_full_name = data.message.first_name + " " + data.message.second_name;
              
            } else if (data.category == "error") {
              this.flashMessage.error({
                message: data.message,
              });
            }
          })
          .catch((error) => {
            reject("Internal Server Error");
          });
      }

      if (this.resolved_by != 0) {
        fetch(common.USERDETAILS_API + `/${this.resolved_by}`, {
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
              
              this.resolved_by_full_name = data.message.first_name + " " + data.message.second_name;
              
            } else if (data.category == "error") {
              this.flashMessage.error({
                message: data.message,
              });
            }
          })
          .catch((error) => {
            reject("Internal Server Error");
          });
      }
    },
    getComments() {
      fetch(common.COMMENTS_API + `/${this.id}`, {
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
            console.log("Ticket Comments Retrived")
            this.comments = data.message;
            console.log(this.comments);
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
    addComment() {
      fetch(common.COMMENTS_API + `/${this.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          webtoken: this.$store.getters.get_web_token,
          userid: this.user_id,
        },
        body: JSON.stringify({
          comment: this.comment_input,
          commenter: this.$store.getters.get_user_name,
          user_mentions: [],
          reactions: "",
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.flashMessage.success({
              message: "Commented!",
            });
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
    commentsVisible() {
      if (this.user_role == "staff" || this.user_role == "admin") {
        this.showComments = true;
      }
    },
    escalateTicket() {
      if (this.already_escalated == false) {
        fetch(common.TRACKING_API + `/${this.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            webtoken: this.$store.getters.get_web_token,
            userid: this.user_id,
          },
          body: JSON.stringify({
            resolved_at: "",
            assigned_at: "",
            inProgress_at: "",
            closed_at: "",
            reopened_at: Date.now(),
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.category == "success") {
              this.flashMessage.success({
                message: "Escalated Ticket",
              });
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
        fetch(common.TRACKING_API + `/${this.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            webtoken: this.$store.getters.get_web_token,
            userid: this.user_id,
          },
          body: JSON.stringify({
            resolved_at: "",
            assigned_at: "",
            inProgress_at: "",
            closed_at: "",
            reopened_at: Date.now(),
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.category == "success") {
              this.flashMessage.success({
                message: "Escalated Ticket",
              });
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

        this.already_escalated = true;
      }
    },
    // getTrackingData() {
    //   console.log(this.tracking_data)
    //   fetch(common.TRACKING_API + `/${this.id}`, {
    //     method: "GET",
    //     headers: {
    //       "Content-Type": "application/json",
    //       webtoken: this.$store.getters.get_web_token,
    //       userid: this.user_id,
    //     },
    //   })
    //     .then((response) => response.json())
    //     .then((data) => {
    //       if (data.category == "success") {
    //         this.flashMessage.success({
    //           message: "",
    //         });
    //         this.tracking_data = data.message;
    //       }
    //       if (data.category == "error") {
    //         this.flashMessage.error({
    //           message: data.message,
    //         });
    //       }
    //     })
    //     .catch((error) => {
    //       this.$log.error(`Error : ${error}`);
    //       this.flashMessage.error({
    //         message: "Internal Server Error",
    //       });
    //     });
    // },
  },
  computed: {},
};
</script>

<style scoped>
.ticket-card-container {
  box-shadow: 2px 4px 5px 5px #dbdada;
  background-color: rgb(251, 252, 252);
  margin: 12px 5px;
}
.ticket-card-container:hover {
  box-shadow: 5px 8px 8px 10px #888888;
  background-color: rgb(255, 255, 255);
}

.ticket-card-buttons {
  border-color: #ffffff;
}
.ticket-card-buttons:hover:not([disabled]) {
  border-color: #95ddfa;
  box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24),
    0 17px 50px 0 rgba(0, 0, 0, 0.19);
}

.ticket-section {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f0f0f0; /* Default background color */
}

.ticket-indicator {
  width: 100%;
  display: flex;
  flex-flow: row wrap;
  justify-content: center;
  margin-bottom: 10px;
}

.row {
  padding-top: 5px;
  padding-bottom: 5px;
}

.dark-bg {
  background-color: #f0f0f0; /* Slightly darker color */
  padding: 5px;
  border-radius: 5px;
  margin-right: 10px;
}

.light-bg {
  background-color: #f9f9f9; /* Slightly lighter color */
  padding: 5px;
  border-radius: 5px;
}

.border-item {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
}

.border-item:not(:last-child) {
  margin-right: 10px; /* Small gap between items */
}

.green-bg {
  background-color: #9fdf9f; /* Green color when resolved */
}
</style>
