<template>
    <div class="ticket-form" 
    style="margin-top: 5px; margin-left: 5px; margin-right: 5px; text-align: left">
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group>
          <b-form-input
            id="input-title"
            v-model="form.title"
            type="text"
            placeholder="Enter Ticket Title"
            :state="check_title"
            required
          ></b-form-input>
          <b-form-invalid-feedback>
            Title should be at least 5 characters long.
          </b-form-invalid-feedback>
        </b-form-group>
  
        <b-form-group>
          <b-form-textarea
            id="input-description"
            v-model="form.raw"
            type="text"
            placeholder="Enter Ticket Description (You can use markdown syntax)"
            :state="check_description"
            rows="3"
            max-rows="8"
            required
          ></b-form-textarea>
          <b-form-invalid-feedback>
            Description should be at least 50 characters long.
          </b-form-invalid-feedback>
        </b-form-group>
  
        <b-form-group>
        <Tags v-model="form.tags" />
        </b-form-group>

        <b-form-group>
        <Category v-model="form.category" />
        </b-form-group>

        <b-form-group>
        <Subcategory :category="form.subCategory" v-model="form.subcategory" />
        </b-form-group>

        <FileUpload @file_uploading="onFileUpload"></FileUpload>
  
        <br />
  
        <b-button style="margin: 10px" type="submit" variant="primary">Submit</b-button>
        <b-button style="margin: 10px" type="reset" variant="danger">Reset</b-button>
      </b-form>
    </div>
  </template>
  
  <script>
  import * as common from "../assets/common.js";
  import FileUpload from "./FileUpload.vue";
  import Category from './CategoryDiscourse.vue';
  import Subcategory from './SubCategoryDiscourse.vue';
  import Tags from './TagsDiscourse.vue';
  
  export default {
    name: "DiscourseTicketForm",
    props: [],
    data() {
      return {
        form: {
          title: "",
          raw: "",
          category:"",
          sub_category:"",
          tags:"",
        },
        show: true,
        user_id: this.$store.getters.get_user_id,
        files:null,
      };
    },
    methods: {
        onFileUpload(value) {
        this.files.push(...value);
    },
      onSubmit(event) {
        if (event && event.preventDefault) {
          event.preventDefault();
        }
  
        if (this.check_title && this.check_description) {
          alert('Submitting Discourse Thread form. Click "Ok" to proceed?');
          this.$log.info("Submitting Discourse ticket form");
  
          this.form.created_by = this.user_id.toString();
          console.log("Form data:", this.form);
          const formData = new FormData();
         formData.append('title', this.form.title);
         formData.append('raw', this.form.raw);
         formData.append('category',this.form.category);
         formData.append('sub_category',this.form.sub_category);
         formData.append('tags',this.form.tags);
                // Append files to FormData object
      if (this.files) {
        for (let i = 0; i < this.files.length; i++) {
          const file = this.files[i];
          // Append each file with a unique key (e.g., 'file0', 'file1', etc.)
          formData.append(`file${i}`, file);
        }
      }
          // Adjust API endpoint for creating discourse ticket
          fetch(common.DISCORD_TICKET_API, {
            method: "POST",
            headers: {
              "Content-Type": "multipart/form-data",
              webtoken: this.$store.getters.get_web_token,
              userid: this.user_id,
            },
             body: formData,
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
        } else {
          alert("Please fill in all required fields.");
        }
      },
      onReset(event) {
        if (event && event.preventDefault) {
          event.preventDefault();
        }
        this.form.title = "";
        this.form.raw = "";
        this.form.category="";
        this.form.sub_category="";
        this.form.tags="";
        this.show = false;
        this.$nextTick(() => {
          this.show = true;
        });
      },
    },
    computed: {
      check_title() {
        return this.form.title.length > 15 ? true : false;
      },
      check_description() {
        return this.form.description.length > 80 ? true : false;
      },
    },
  };
  </script>
  
  <style></style>
  