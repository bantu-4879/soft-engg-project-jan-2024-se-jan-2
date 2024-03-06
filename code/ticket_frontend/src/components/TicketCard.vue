<template>
  <div>
    <template v-if="ticket_id">
      <b-container
        class="ticket-card-container"
        v-show="!ticket_deleted"
        :style="[
          user_id == created_by && $route.path == '/student-create-ticket'
            ? { 'background-color': 'rgb(225, 245, 250)' }
            : { 'background-color': 'rgb(251, 252, 252)' },
        ]"
      >
        <!-- Stack the columns on mobile by making one full-width and the other half-width -->
        <b-row class="row" @click="getTicketDetails">
          <b-col class="col" cols="12" lg="5" sm="12"
            ><i>Id: </i>{{ ticket_id.slice(0, 15) }}</b-col
          >
          <b-col class="col" cols="12" lg="5" sm="8"><i>Created On: </i>{{ created_on }}</b-col>
          <b-col class="col" cols="12" lg="2" sm="4"><i>Votes: </i>{{ votes }}</b-col>
        </b-row>
        <b-row class="row">
          <b-col class="col" cols="12" sm="10" lg="11" @click="getTicketDetails">
            <b-row class="row">
              <b-col class="col" cols="12"><b>Title: </b>{{ title.slice(0, 80) }}</b-col>
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
                      : user_id !== created_by && user_role == 'student' && !is_resolved
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
                  @click="showEditTicketModal"
                  variant="outline-light"
                  size="sm"
                  class="ticket-card-buttons"
                  :disabled="edit_disabled"
                  v-show="
                    edit_disabled
                      ? !edit_disabled
                      : (user_id == created_by || user_role == 'support') && !is_resolved
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
                  v-show="delete_disabled ? !delete_disabled : user_id == created_by"
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
        <span style="font-size: 20px">Ticket ID: {{ ticket_id }}</span>
        <b-button size="sm" variant="outline-danger" @click="cancel()"> Close </b-button>
      </template>

      <div class="d-block text-left">
        <h5 style="text-align: center">Ticket Details</h5>
        <!-- display as a table -->
        <table style="width: 100%">
          <tr>
            <th style="width: 15%">Attribute</th>
            <th>Details</th>
          </tr>
          <tr>
            <td>Title:</td>
            <td>{{ title }}</td>
          </tr>
          <tr>
            <td>Description:</td>
            <td>{{ description }}</td>
          </tr>
          <tr>
            <td>Status:</td>
            <td>{{ status }}</td>
          </tr>
          <tr>
            <td>Priority:</td>
            <td>{{ priority }}</td>
          </tr>
          <tr>
            <td>Tags:</td>
            <td>{{ tag_1 + tag_2 + tag_3 }}</td>
          </tr>
          <tr>
            <td>Votes:</td>
            <td>{{ votes }}</td>
          </tr>
          <tr>
            <td>Created on:</td>
            <td>{{ Date(created_on).toLocaleString() }}</td>
          </tr>
          <tr>
            <td>Created by:</td>
            <td>{{ created_by }}</td>
          </tr>
          <tr>
            <td>Resolved by:</td>
            <td>{{ resolved_by ? resolved_by : "" }}</td>
          </tr>
          <tr>
            <td>Resolved on:</td>
            <td>{{ resolved_on == 0 ? "" : Date(resolved_on).toLocaleString() }}</td>
          </tr>
          <tr>
            <td>Solution:</td>
            <td>{{ solution }}</td>
          </tr>
        </table>
        <div>
          <p>Attachments</p>
          <div v-for="(attach, imageIndex) in attachments" :key="imageIndex">
            <img :src="attach.attachment_loc" class="img-fluid" />
          </div>
        </div>
      </div>

      <template #modal-footer="{ cancel }">
        <b-button size="sm" variant="danger" @click="cancel()"> Cancel </b-button>
      </template>
    </b-modal>

    <b-modal
      :id="delete_ticket_modal_id"
      @cancel="$bvModal.hide(delete_ticket_modal_id)"
      @ok="deleteTicket"
      size="sm"
      scrollable
    >
      <template #modal-header="{ cancel }">
        <span style="font-size: 20px">Delete Ticket ?</span>
        <b-button size="sm" variant="outline-danger" @click="cancel()"> Close </b-button>
      </template>

      <template #modal-footer="{ ok, cancel }">
        <b-button size="sm" variant="secondary" @click="cancel()"> Cancel </b-button>
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
        <span style="font-size: 20px">Ticket ID: {{ ticket_id }}</span>
        <b-button size="sm" variant="outline-danger" @click="cancel()"> Close </b-button>
      </template>

      <div class="d-block text-left">
        <h5 style="text-align: center">Edit Ticket Details</h5>
        <!-- display as a table -->
        <TicketForm
          :ticket_id="ticket_id"
          :title="title"
          :description="description"
          :priority="priority"
          :tags="tags"
          :hideReset="true"
          :editTicket="true"
          @ticketResolved="ticketResolvedFn"
        ></TicketForm>
      </div>

      <template #modal-footer="{ cancel }">
        <b-button size="sm" variant="secondary" @click="cancel()"> Cancel </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import * as common from "../assets/common.js";
import TicketForm from "../components/TicketForm.vue";

export default {
  name: "TicketCard",
  props: [
    "ticket_id",
    "created_on",
    "created_by",
    "title",
    "description",
    "votes",
    "upvote_disabled",
    "delete_disabled",
    "edit_disabled",
    "is_resolved",
  ],
  components: { TicketForm },
  data() {
    return {
      button_1_active: false,
      user_id: this.$store.getters.get_user_id,
      user_role: this.$store.getters.get_user_role,
      show_ticket_modal_id: "show_ticket_modal_" + this.ticket_id,
      edit_ticket_modal_id: "edit_ticket_modal_" + this.ticket_id,
      delete_ticket_modal_id: "delete_ticket_modal_" + this.ticket_id,
      priority: "",
      status: "",
      solution: "",
      resolved_by: "",
      resolved_on: "",
      tag_1: "",
      tag_2: "",
      tag_3: "",
      tags: [],
      attachments: [],
      ticket_deleted: false,
    };
  },
  created() {},
  mounted() {},
  methods: {
    ticketResolvedFn() {
      this.ticket_deleted = true; // its not deletd, its resolved , so its hidden
    },
    getTicketDetails() {
      fetch(common.TICKET_API + `/${this.ticket_id}` + `/${this.created_by}`, {
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
            // load data
            this.title = data.message.title;
            this.description = data.message.description;
            this.votes = data.message.votes;
            this.priority = data.message.priority;
            this.status = data.message.status;
            this.solution = data.message.solution;
            this.resolved_by = data.message.resolved_by;
            this.resolved_on = data.message.resolved_on;
            this.tag_1 = data.message.tag_1;
            this.tag_2 = data.message.tag_2 ? ", " + data.message.tag_2 : "";
            this.tag_3 = data.message.tag_3 ? ", " + data.message.tag_3 : "";
            this.tags = [];
            if (this.tag_1) {
              this.tags.push(this.tag_1);
            }
            if (this.tag_2) {
              this.tags.push(this.tag_2);
            }
            if (this.tag_3) {
              this.tags.push(this.tag_3);
            }
            this.attachments = data.message.attachments;
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
    upvoteTicket() {
      if (this.user_id == this.created_by) {
        this.flashMessage.error({
          message: "Can't upvote own ticket.",
        });
      } else {
        fetch(common.TICKET_API + `/${this.ticket_id}` + `/${this.user_id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            web_token: this.$store.getters.get_web_token,
            user_id: this.user_id,
          },
          body: JSON.stringify({}),
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
      fetch(common.TICKET_API + `/${this.ticket_id}` + `/${this.user_id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          web_token: this.$store.getters.get_web_token,
          user_id: this.user_id,
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
.row {
  padding-top: 5px;
  padding-bottom: 5px;
}
.ticket-card-buttons {
  border-color: #ffffff;
}
.ticket-card-buttons:hover:not([disabled]) {
  border-color: #95ddfa;
  box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19);
}
</style>
