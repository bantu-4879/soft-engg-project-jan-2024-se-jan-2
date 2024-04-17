<template>
    <div>
      <b-form-select v-model="selectedTags" multiple @change="emitSelectedTags">
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
        user_id:this.$store.getters.get_user_id,
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
              console.log("cannot retrieve tags.");
            });
      },
      formatSelectedTags() {
        return this.selectedTags.map(tag => {
    return tag.name;
  })
      },
      emitSelectedTags() {
      this.$emit('selected-tags', this.selectedTags);
    },
    },
  };
  </script>
  