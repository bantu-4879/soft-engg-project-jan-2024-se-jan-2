<template>
  <div class="login-form">
    <div style="margin: 3%; padding: 3%; width: 50%">
      <h3 style="text-align: left">Login</h3>
      <br />
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group
          ><b-form-input
            id="input-email-login"
            v-model="form.email"
            type="email"
            placeholder="Enter email"
            required
          ></b-form-input
        ></b-form-group>

        <b-form-group
          ><b-form-input
            id="input-password-login"
            v-model="form.password"
            placeholder="Enter password"
            type="password"
            required
          ></b-form-input
        ></b-form-group>
        <br />
        <b-button style="margin: 10px" type="submit" variant="primary">Submit</b-button>
        <b-button style="margin: 10px" type="reset" variant="danger">Reset</b-button>
      </b-form>
      <br />

      <p>New user? Please <b-link href="/register">Register here</b-link></p>
      <p>Go to <b-link href="/home">Home Page</b-link></p>
    </div>
  </div>
</template>

<script>
import * as common from "../assets/common.js";

export default {
  name: "LoginView",
  components: {},
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      show: true,
    };
  },
  methods: {
    onSubmit: async function (event) {
      event.preventDefault();
      this.$log.info("Submitting Login form");
      this.form.password = btoa(this.form.password);

      fetch(common.AUTH_API_LOGIN, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.form),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.flashMessage.success({
              message: "Successfully logged in.",
            });

            // update store
            this.$store.dispatch("set_state_after_login", data.message);
            this.$store.dispatch("token_timeout_fn", {});
            this.$router.push(`/${data.message.role}-home`); //home page depends on role
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
      this.form.email = "";
      this.form.password = "";
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>

<style></style>

