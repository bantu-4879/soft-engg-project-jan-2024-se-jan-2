
<template>
    <div>
      <label for="category">Select Category:</label>
      <select v-model="selectedCategory" @change="handleChange">
        <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
      </select>
    </div>
  </template>
  
  <script>
  import * as common from "../assets/common.js";
  
  export default {
    name:"Category",
    props: ['value'], 
    data() {
      return {
        selectedCategory: this.value || '', 
        categories: [], 
      };
    },
    created() {
      this.fetchCategories();
    },
    methods: {
      fetchCategories() {
        fetch(common.DISCOURSE_TICKET_API + '/categories', {
            method: "GET",
            headers: {
              webtoken: this.$store.getters.get_web_token,
              userid: this.user_id,
            }
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.category == "success") {
                this.categories=data.message
                console.log(" categories are being rendered.")
                this.flashMessage.success({
                  message: "Categories Retrieved successfully",
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

      },
      handleChange() {
        this.$emit('input', this.selectedCategory);
      },
    },
  };
  </script>
  