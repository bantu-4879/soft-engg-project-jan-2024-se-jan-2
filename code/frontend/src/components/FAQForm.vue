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
        tags: [],
        tag_1: "",
        tag_2: "",
        tag_3: "",
        attachments: [],
        created_by: "",
      },
      show: true,
      user_id: this.$store.getters.get_user_id,
    };
  },
  created() {},
  methods: {
    onFileUpload(value) {
      this.form.attachments.splice(0, this.form.attachments.length, ...value);
    },
    onSubmit(event) {
      if (event && event.preventDefault) {
        event.preventDefault();
      }

      if (this.form.tags.length == 0 && this.check_question && this.check_solution) {
        alert(
          "Choose atleast 1 tag, question should be atleast 5 characters long and solution should be 5 character long."
        );
      } else {
        alert('Submitting form. Click "Ok" to proceed?');
        this.$log.info("Submitting FAQ form");

        for (let i in this.form.tags) {
          if (this.form.tags[i]) {
            this.form[`tag_${parseInt(i) + 1}`] = this.form.tags[i];
          }
        }

        this.form.created_by = this.user_id.toString();

        fetch(common.FAQ_API, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            web_token: this.$store.getters.get_web_token,
            user_id: this.user_id,
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
      this.form.tags = [];
      this.form.tag_1 = "";
      this.form.tag_2 = "";
      this.form.tag_3 = "";
      this.form.attachments = [];
      this.form.created_by = "";
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
