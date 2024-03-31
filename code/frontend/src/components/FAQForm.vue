<template>
  <div
    class="faq-form"
    style="margin-top: 5px; margin-left: 5px; margin-right: 5px; text-align: left"
  >
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        ><b-form-input
          id="input-question"
          v-model="form.question"
          type="text"
          placeholder="Enter Question"
          :state="check_question"
          aria-describedby="input-live-feedback-title"
          required
        ></b-form-input>
        <b-form-invalid-feedback id="input-live-feedback-title">
          Question should be atleast 5 characters long.
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        ><b-form-textarea
          id="input-solution"
          v-model="form.solution"
          type="text"
          placeholder="Enter Solution"
          :state="check_solution"
          rows="3"
          max-rows="6"
        ></b-form-textarea>
        <b-form-invalid-feedback id="input-live-feedback-title">
          Solution should be atleast 5 characters long.
        </b-form-invalid-feedback>
      </b-form-group>

      <Tagging @tags_changed="onTagsChanged"></Tagging>

      <FileUpload @file_uploading="onFileUpload"></FileUpload>

      <br />

      <br />
      <b-button style="margin: 10px" type="submit" variant="primary">Submit</b-button>
      <b-button style="margin: 10px" type="reset" variant="danger">Reset</b-button>
    </b-form>
    <br />

    <!-- <b-card class="mt-3" header="Form Data : Temporary">
      <pre class="m-0">{{ form }}</pre>
    </b-card> -->
  </div>
</template>

<script>
import * as common from "../assets/common.js";
import FileUpload from "./FileUpload.vue";
import Tagging from "./Tagging.vue";

export default {
  name: "FAQForm",
  props: [],
  components: { Tagging, FileUpload },
  data() {
    return {
      form: {
        question: "",
        solution: "",
        tags_list: [],
        created_by: "",
        attachments: [],
      },
      show: true,
      user_id: this.$store.getters.get_user_id,
    };
  },
  created() {},
  methods: {
    onFileUpload(value) {
      this.form.attachments.splice(0, this.form.attachments.length, ...value);
      console.log("Attachments uploaded:", this.form.attachments);
    },
    onSubmit(event) {
      if (event && event.preventDefault) {
        event.preventDefault();
      }

      if (this.form.tags_list.length == 0 && this.check_question == false && this.check_solution == false) {
        alert(
          "Choose atleast 1 tag, question should be atleast 5 characters long and solution should be 5 character long."
        );
      } else {
        alert('Submitting form. Click "Ok" to proceed?');
        this.$log.info("Submitting FAQ form");


        this.form.created_by = this.user_id.toString();
        console.log("Form data:", this.form);

        fetch(common.FAQ_API, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            webtoken: this.$store.getters.get_web_token,
            userid: this.user_id,
          },
          body: JSON.stringify(this.form),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.category == "success") {
              this.flashMessage.success({
                message: data.message,
              });
              this.onReset();
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
      this.form.question = "";
      this.form.solution = "";
      this.form.tags_list = [];
      this.form.attachments = [];
      this.form.created_by = "";
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    onTagsChanged(value) {
      this.form.tags_list = value;
      console.log("Tags changed:", this.form.tags_list);
    },
  },
  computed: {
    check_question() {
      return this.form.question.length > 5 ? true : false;
      
    },
    check_solution() {
      return this.form.solution.length > 5 ? true : false;
    },
  },
};
</script>

<style></style>
