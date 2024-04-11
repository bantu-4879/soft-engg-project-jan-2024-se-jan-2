<template>
  <div class="user-card-container" v-if="this.show_component">
    <b-list-group>
      <b-list-group-item class="d-flex justify-content-between align-items-center">
        Name: {{ first_name }} {{ last_name }}
        <b-button @click="verify_user" variant="outline-light">
          <b-icon icon="check-square" scale="2" variant="success"></b-icon>
        </b-button>
      </b-list-group-item>
      <b-list-group-item class="d-flex justify-content-between align-items-center">
        Email: {{ email }}
        <b-button @click="not_verify_user" variant="outline-light">
          <b-icon icon="x-circle" scale="2" variant="danger"></b-icon>
        </b-button>
      </b-list-group-item>
    </b-list-group>
    <b-list-group-item class="d-flex justify-content-between align-items-center">
      Role: {{ role }}
    </b-list-group-item>
  </div>
</template>

<script>
import * as common from "../assets/common.js";
export default {
  name: "UserCard",
  props: ["n_user_id", "first_name", "last_name", "email", "role", "show"],
  components: {},
  data() {
    return {
      user_id: this.$store.getters.get_user_id,
      new_user_id: this.n_user_id,
      show_component: this.show,
    };
  },
  created() {},
  mounted() {},
  methods: {
    init() {
      this.new_user_id = this.n_user_id;
    },
    not_verify_user: async function (event) {
      fetch(common.AUTH_API_NEWUSERS + `/${this.new_user_id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          webtoken: this.$store.getters.get_web_token,
          userid: this.user_id,
        },
        body: JSON.stringify({
          user_id: this.new_user_id,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.flashMessage.success({
              message: "Verification Declined",
            });
            this.show_component = false;
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

      if(this.role == "student") {
        let webhook_url = common.WEBHOOK_URL_STUDENT;
        let webhook_message = {
          "cards": [
            {
              "header": {
                "title": "Student Not Verified",
                "subtitle": "Name: " + this.first_name + " " + this.last_name,
                "imageUrl": "https://e7.pngegg.com/pngimages/598/398/png-clipart-jerry-of-tom-and-jerry-illustration-jerry-mouse-tom-cat-tom-and-jerry-cartoon-other-other-mammal.png", // Optional: You can include an image URL here
              },
              "sections": [
                {
                  "widgets": [
                    {
                      "keyValue": {
                        "topLabel": "Role",
                        "content": this.role,
                        "contentMultiline": false
                      }
                    }
                  ]
                },
                {
                  "widgets": [
                    {
                      "textParagraph": {
                        "text": "Message: " + "Your id is not verfied by admin. You can not login to the system."
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
                message: "Notified verification update to student",
              });
          })
        
      }

      if(this.role == "staff") {
      let webhook_url = common.WEBHOOK_URL_STAFF;
      let webhook_message = {
        "cards": [
          {
            "header": {
              "title": "Staff Not Verified",
              "subtitle": "Name: " + this.first_name + " " + this.last_name,
              "imageUrl": "https://e7.pngegg.com/pngimages/598/398/png-clipart-jerry-of-tom-and-jerry-illustration-jerry-mouse-tom-cat-tom-and-jerry-cartoon-other-other-mammal.png", // Optional: You can include an image URL here
            },
            "sections": [
              {
                "widgets": [
                  {
                    "keyValue": {
                      "topLabel": "Role",
                      "content": this.role,
                      "contentMultiline": false
                    }
                  }
                ]
              },
              {
                "widgets": [
                  {
                    "textParagraph": {
                      "text": "Message: " + "Your id is not verfied by admin. You can not login to the system."
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
              message: "Notified verification update to staff",
            });
        })
        
      }
    },
    verify_user: async function (event) {
      event.preventDefault();

      fetch(common.AUTH_API_NEWUSERS + `/${this.new_user_id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          webtoken: this.$store.getters.get_web_token,
          userid: this.user_id,
        },
        body: JSON.stringify({
          user_id: this.new_user_id,
          verified: "true",
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.flashMessage.success({
              message: "Successfully Verified",
            });
            this.show_component = false;
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
        
      if(this.role == "student") {
      let webhook_url = common.WEBHOOK_URL_STUDENT;
      let webhook_message = {
        "cards": [
          {
            "header": {
              "title": "Student Verified",
              "subtitle": "Name: " + this.first_name + " " + this.last_name,
              "imageUrl": "https://e7.pngegg.com/pngimages/598/398/png-clipart-jerry-of-tom-and-jerry-illustration-jerry-mouse-tom-cat-tom-and-jerry-cartoon-other-other-mammal.png", // Optional: You can include an image URL here
            },
            "sections": [
              {
                "widgets": [
                  {
                    "keyValue": {
                      "topLabel": "Role",
                      "content": this.role,
                      "contentMultiline": false
                    }
                  }
                ]
              },
              {
                "widgets": [
                  {
                    "textParagraph": {
                      "text": "Message: " + "Your id is verfied by admin. You can now login to the system."
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
              message: "Notified verification update to student",
            });
        })
        
      }

      if(this.role == "staff") {
      let webhook_url = common.WEBHOOK_URL_STAFF;
      let webhook_message = {
        "cards": [
          {
            "header": {
              "title": "Staff Verified",
              "subtitle": "Name: " + this.first_name + " " + this.last_name,
              "imageUrl": "https://e7.pngegg.com/pngimages/598/398/png-clipart-jerry-of-tom-and-jerry-illustration-jerry-mouse-tom-cat-tom-and-jerry-cartoon-other-other-mammal.png", // Optional: You can include an image URL here
            },
            "sections": [
              {
                "widgets": [
                  {
                    "keyValue": {
                      "topLabel": "Role",
                      "content": this.role,
                      "contentMultiline": false
                    }
                  }
                ]
              },
              {
                "widgets": [
                  {
                    "textParagraph": {
                      "text": "Message: " + "Your id is verfied by admin. You can now login to the system."
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
              message: "Notified verification update to staff",
            });
        })
        
      }
    },
  },
  computed: {},
};
</script>

<style scoped>
.user-card-container {
  box-shadow: 2px 4px 5px 5px #dbdada;
  /* background-color: rgb(251, 252, 252); */
  margin: 12px 15px;
  /* padding: 10px; */
}
/* .info-card-container:hover {
  box-shadow: 5px 8px 8px 10px #888888;
   background-color: rgb(255, 255, 255); 
} */
</style>
