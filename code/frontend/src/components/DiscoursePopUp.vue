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
            Description should be at least 30 characters long.
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group>
        <Category v-model="form.category" />
        </b-form-group>

        <b-form-group>
        <Tags v-model="form.tags" @selected-tags="handleSelectedTags" />
        </b-form-group>

        <b-form-group>
        <div>
        <input type="file" multiple ref="fileInput" @change="handleFileChange">
      </div>
        </b-form-group>

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
  import Tags from './TagsDiscourse.vue';
  import axios from 'axios';
  
  export default {
    name: "DiscourseTicketForm",
    props: ["id", "title", "description"],
    components: { FileUpload ,Category,Tags},
    data() {
      return {
        form: {
          title: this.title ? this.title : "",
          raw: this.description ? this.description : "",
          category:"",
          tags:"",
        },
        show: true,
        user_id: this.$store.getters.get_user_id,
        files:null,
      };
    },
    mounted()
    {
        console.log(this.id);
    },
    methods: {
      handleFileChange() {
      const input = this.$refs.fileInput;

      this.files = Array.from(input.files);
    },
      onSubmit(event) {
        if (event && event.preventDefault) {
          event.preventDefault();
        }
  
        if (this.check_title && this.check_description) {
          alert('Submitting Discourse Thread form. Click "Ok" to proceed?');
          this.$log.info("Submitting Discourse ticket form");
          console.log(this.id);
          console.log("Form data:", this.form);
        const formData = new FormData();
         formData.append('title', this.form.title);
         formData.append('raw', this.form.raw);
         formData.append('category',this.form.category);
         formData.append('tags',this.form.tags);
        console.log(formData);
      if (this.files) {
        for (let i = 0; i < this.files.length; i++) {
          const file = this.files[i];
          formData.append('files', file,file.name);
        }
      }
          const url = `${common.DISCOURSE_TICKET_API}/topic/${this.user_id}/${this.id}`;
          axios.post(url, formData, {
            headers: {
              'Content-Type': 'multipart/form-data', // Set explicitly for clarity
              webtoken: this.$store.getters.get_web_token,
              userid: this.user_id,
            }
          })
          .then(response => response.data)
          .then(data => {
            if (data.category === "success") {
              this.flashMessage.success({ message: "Discourse Thread successfully created." });
              this.onReset();
              this.$emit("DiscourseTopicCreated")
            } else if (data.category === "error") {
              this.flashMessage.error({ message: data.message });
            }
          })
          .catch(error => {
            this.$log.error(`Error : ${error}`);
            this.flashMessage.error({ message: "Internal Server Error" });
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
        this.form.tags="";
        this.show = false;
        this.$nextTick(() => {
          this.show = true;
        });
      },
      handleSelectedTags(selectedTags) {
      console.log("Selected tags:", selectedTags);
      this.form.tags=selectedTags
    },
    },
    computed: {
      check_title() {
        return this.form.title.length > 15 ? true : false;
      },
      check_description() {
        return this.form.raw.length > 30 ? true : false;
      },
    },
  };
  </script>
  
  <style></style>
  