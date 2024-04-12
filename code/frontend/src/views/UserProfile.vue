<template>
  <div>
    <UserNavbar :id_="0"></UserNavbar>
    <b-container fluid="xl">
      <b-container fluid="xl">
        <div>
        </br>
          <h3>{{ user_name.toUpperCase() }}</h3>
          <h4><i>{{ discplinary_action_card }}</i></h4>
          <h4>{{ user_badges.join(', ') }}</h4>
        </div>
      </b-container>
      <b-row class="text-start"  style="border-bottom: dashed black">
        <b-col cols="12" sm="7" md="7" style="border-right: dashed black">
          <h3 style="text-align: center">My Profile</h3>
          <div
            class="profile-form"
            style="
              margin-top: 5px;
              margin-left: 5px;
              margin-right: 5px;
              text-align: left;
            "
          >
            <b-form @submit="onSubmit" @reset="onReset" v-if="show">
              <b-form-group
                label="First Name:"
                label-for="input-first-name-change"
                ><b-form-input
                  id="input-first-name-change"
                  v-model="form.first_name"
                  type="text"
                  placeholder="Enter first name"
                  :state="check_name"
                  aria-describedby="input-live-feedback-first-name"
                  required
                ></b-form-input>
                <b-form-invalid-feedback id="input-live-feedback-first-name">
                  Enter at least 3 letters of first name
                </b-form-invalid-feedback>
              </b-form-group>
              <b-form-group
                label="Last Name:"
                label-for="input-last-name-change"
                ><b-form-input
                  id="input-last-name-change"
                  v-model="form.second_name"
                  type="text"
                  placeholder="Enter Second name (Optional)"
                ></b-form-input
              ></b-form-group>

              <b-form-group label="Email:" label-for="input-email-change"
                ><b-form-input
                  id="input-email-change"
                  v-model="form.email"
                  type="email"
                  placeholder="Enter email"
                  required
                ></b-form-input
              ></b-form-group>

              <b-form-group label="Password:" label-for="input-password-change"
                ><b-form-input
                  id="input-password-change"
                  v-model="form.password"
                  placeholder="Enter new password"
                  type="password"
                  :state="check_password"
                  aria-describedby="input-live-feedback-password"
                ></b-form-input>
                <b-form-invalid-feedback id="input-live-feedback-password">
                  Password should contain letters A-Z a-z and numbers 0-9 only
                  and should be atleast 4 and atmost 8 characters long.
                </b-form-invalid-feedback>
              </b-form-group>

              <b-form-group
                ><b-form-input
                  id="input-retype-password-change"
                  v-model="form.retype_password"
                  placeholder="Retype new password"
                  type="password"
                  :state="check_retype_password"
                  aria-describedby="input-live-feedback-retype-password"
                ></b-form-input>
                <b-form-invalid-feedback
                  id="input-live-feedback-retype-password"
                >
                  Password did not match.
                </b-form-invalid-feedback>
              </b-form-group>
              <b-button style="margin: 10px" type="submit" variant="primary"
                >Update</b-button
              >
              <b-button style="margin: 10px" type="reset" variant="danger"
                >Reset</b-button
              >
            </b-form>
          </div>
        </b-col>
        <b-col cols="12" sm="5" md="5" style="padding-top: 10px">
          <b-img
            :src="form.profile_photo_loc"
            v-bind="imageProps"
            alt="Profile image"
            rounded="circle"
          ></b-img>
          <br />

          <FileUpload @file_uploading="onFileUpload"></FileUpload>
          <p>Click 'Update' to set this as new profile picture</p>
        </b-col>
      </b-row class="text-start">
      <div v-if="!isregisteredOnDiscourse">
      <div 
            class="profile-form"
            style="margin-top: 5px; margin-left: 5px; margin-right: 5px; text-align: left">
          <h3 style="text-align: center">Discourse Registration</h3>
          <b-form @submit="registerDiscourse" @reset="onResetDiscourse">
        <b-form-group label="Name:" label-for="input-name">
          <b-form-input
            id="input-name"
            v-model="discourse_form.name"
            type="text"
            placeholder="Enter your name"
            :state="check_name2"
            aria-describedby="input-live-feedback-name"
            required
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback-name">
            Enter at least 3 letters for valid name
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label="Email:" label-for="input-email-discourse">
          <b-form-input
            id="input-email-discourse"
            v-model="discourse_form.email_id"
            type="email"
            placeholder="Enter email id for discourse"
            required
          ></b-form-input>
        </b-form-group >
        <b-form-group label="Username" label-for="input-username-discourse">
          <b-form-input
            id="input-username-discourse"
            v-model="discourse_form.username"
            placeholder="Enter Username"
            type="text"
          ></b-form-input>
        </b-form-group>
        <b-form-group label="Password:" label-for="input-discourse-password">
          <b-form-input
            id="input-password"
            v-model="discourse_form.password"
            placeholder="Enter password"
            type="password"
            :state="check_password2"
            aria-describedby="input-live-feedback-discourse-password"
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback-discourse-password">
            Password should contain letters A-Z a-z and numbers 0-9 only and should be at least 8 characters long.
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group>
          <b-form-input
            id="input-retype-password-change"
            v-model="retypePassword"
            placeholder="Retype new password"
            type="password"
            :state="checkRetypePassword"
            aria-describedby="input-live-feedback-retype-discourse-password"
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback-retype-discourse-password">
            Passwords do not match.
          </b-form-invalid-feedback>
        </b-form-group>
        <b-button style="margin: 10px" type="submit" variant="primary">Submit</b-button>
        <b-button style="margin: 10px" type="reset" variant="danger">Reset</b-button>
      </b-form>
          </div>
        </div>
          <div v-else>
            <h3 style="text-align: center">Discourse Registration is complete</h3>
    </div>

      <b-row>

      </b-row>
    </b-container>
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import FileUpload from "../components/FileUpload.vue";
import * as common from "../assets/common.js";

export default {
  name: "UserProfile",
  components: { UserNavbar, FileUpload },
  data() {
    return {
      imageProps: { width: 250, height: 250, center: true },
      user_role: this.$store.getters.get_user_role,
      user_id: this.$store.getters.get_user_id,
      user_url_to_fetch_data: "",
      badge_fetch_url: "",
      discplinary_action_card: "",
      user_name: "",
      user_badges: [],
      form: {
        first_name: "",
        second_name: "",
        email: "",
        password: "",
        retype_password: "",
        profile_photo_loc: "",
      },
      discourse_form:{
        name:"",
        email_id:"",
        password:"",
        username:"",
        user_id:"",
      },
      show: true,
      isregisteredOnDiscourse:false,
      retypePassword: "",
    };
  },
  created() {
    const user = this.$store.getters.get_user;
    this.form.first_name = user.first_name;
    this.form.second_name = user.second_name;
    this.form.email = user.email;
    this.form.profile_photo_loc = this.$store.getters.get_user_profile_pic;
    if (this.user_role === "student") {
      this.user_url_to_fetch_data = common.STUDENT_API + `/${this.user_id}`;
      this.badge_fetch_url =
        common.MANAGEMENT_API + "/badge" + `/${this.user_id}`;
      this.user_badges = ["NA"]
    }
    if (this.user_role === "staff") {
      this.user_url_to_fetch_data = common.SUPPORT_API + `/${this.user_id}`;
      this.discplinary_action_card = "NA"
    }
    if (this.user_role === "admin") {
      this.user_url_to_fetch_data = common.ADMIN_API + `/${this.user_id}`;
    }
    fetch(this.user_url_to_fetch_data, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        web_token: this.$store.getters.get_web_token,
        user_id: this.$store.getters.get_user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.category == "success") {
          this.flashMessage.success({
            message: "Data Retrieved",
          });
          this.discplinary_action_card = data.message.card + " Card";
          this.user_name = data.message.first_name;
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

    //THIS IS THE BADGE FETCH
    fetch(this.badge_fetch_url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        web_token: this.$store.getters.get_web_token,
        user_id: this.$store.getters.get_user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.category == "success") {
          this.flashMessage.success({
            message: "Data Retrieved",
          });
          this.user_badges = data.message;
          
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
    this.isregisteredOnDiscoursefun();
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      alert('You are updating your profile. Click "Ok" to proceed?');
      this.$log.info("Submitting Update Profile form");

      this.form.password = btoa(this.form.password);
      this.form.retype_password = btoa(this.form.retype_password);

      fetch(this.user_url_to_fetch_data, {
        method: "Put",
        headers: {
          "Content-Type": "application/json",
          webtoken: this.$store.getters.get_web_token,
          userid: this.$store.getters.get_user_id,
        },
        body: JSON.stringify(this.form),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.flashMessage.success({
              message: data.message,
            });

            // update store
            this.$store.dispatch("set_state_after_profile_update", this.form);
            this.$forceUpdate();
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
      event.preventDefault();
      const user = this.$store.getters.get_user;
      this.form.first_name = user.first_name;
      this.form.second_name = user.second_name;
      this.form.email = user.email;
      this.form.password = "";
      this.form.retype_password = "";
      this.form.profile_photo_loc = this.$store.getters.get_user_profile_pic;
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
      this.$forceUpdate();
    },
    onFileUpload(value) {
      this.form.profile_photo_loc = value[0].attachment_loc;
    },
    registerDiscourse(event){
      event.preventDefault();
      fetch(common.DISCOURSE_REGISTER_API + '/discourseRegister', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          webtoken: this.$store.getters.get_web_token,
          userid: this.$store.getters.get_user_id,

        },
        body: JSON.stringify({
          email: this.discourse_form.email_id,
          user_id: this.$store.getters.get_user_id,
          password: this.discourse_form.password,
          username: this.discourse_form.username,
          name: this.discourse_form.name,
        }),
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
            message: "Internal Server Error due to discourse",
          });
        });
    }
  },
  isregisteredOnDiscoursefun(){
    console.log("I reached here.")
    this.loading = true;
    user_id= this.$store.getters.get_user_id
      fetch(common.DISCOURSE_REGISTER_API + '/discourseExists'+`/${user_id}`, {
        method: "GET",
        headers: {
          webtoken: this.$store.getters.get_web_token,
          userid: this.user_id,
        },
      }) // Replace `user_id` with the actual user id
        .then(response => {
          if (!response.ok) {
            throw new Error('User not found');
          }
          return response.json();
        })
        .then(data => {
          this.loading = false;
          if (data.username) {
            this.isregisteredOnDiscourse= true;
          } else {
            this.isregisteredOnDiscourse= false;
          }
        })
        .catch((error) => {
          this.$log.error(`Error : ${error}`);
          this.isregisteredOnDiscourse=false;
          this.flashMessage.error({
            message: "Cannot Retrieve Data.",
          });
        });

  },
    onResetDiscourse(event) {
      event.preventDefault();
      this.discourse_form = {
        name: "",
        second_name: "",
        email_id: "",
        password: "",
      };
      this.retypePassword = "";
    },
  computed: {
    check_name() {
      return this.form.first_name.length > 2 ? true : false;
    },
    check_name2()
    {
      return this.discourse_form.name.length > 2 ? true : false;
    },
    check_password() {
      let password = this.form.password;
      if (password.length < 4 || password.length > 9) {
        return false;
      }
      const valid_char_array = Array.from(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
      );
      const password_array = Array.from(password);
      for (let i = 0; i < password_array.length; i++) {
        if (!valid_char_array.includes(password_array[i])) {
          return false;
        }
      }
      return true;
    },
    check_retype_password() {
      return this.form.password === this.form.retype_password && this.check_password ? true : false;
    },
    check_password2() {
      // Password should contain letters A-Z a-z and numbers 0-9 only and should be at least 8 characters long
      const regex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*_).{8,}$/;
      let password2=this.discourse_form.password;
      console.log(regex.test(password2))
      return regex.test(password2);
    },
    checkRetypePassword() {
      return this.retypePassword === this.discourse_form.password && this.check_password2 ? true:false;
    },
  },
};
</script>

<style></style>
