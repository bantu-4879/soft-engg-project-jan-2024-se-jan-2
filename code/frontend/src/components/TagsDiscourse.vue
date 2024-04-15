<template>
    <div>
      <b-form-select v-model="selectedTags" multiple>
        <option v-for="tag in tags" :key="tag.id" :value="tag.name">{{ tag.name }}</option>
      </b-form-select>
    </div>
  </template>
  
  <script>
  import * as common from "../assets/common.js";
  export default {
    name:"Tags",
    data() {
      return {
        selectedTags: [],
        tags: [],
      };
    },
    mounted() {
      this.fetchTags();
    },
    methods: {
      fetchTags() {
        fetch(common.DISCOURSE_TICKET_API + '/tags', {
            method: "GET",
            headers: {
              webtoken: this.$store.getters.get_web_token,
              userid: this.user_id,
            }
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.category == "success") {
                this.tags=data.message.map(tag => ({ id: tag.id, name: tag.name }));
                console.log("Tags are being rendered.")
                this.onReset();
              }
              if (data.category == "error") {
                console.log("cannot retrive messages.")
              }
            })
            .catch((error) => {
              this.$log.error(`Error : ${error}`);
              this.flashMessage.error({
                message: "Internal Server Error",
              });
            });
      },
      formatSelectedTags() {
        return this.selectedTags.map(tag => tag.name);
      },
    },
  };
  </script>
  