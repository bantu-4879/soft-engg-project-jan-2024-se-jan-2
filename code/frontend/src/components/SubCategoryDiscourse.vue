<template>
    <div>
      <label for="subcategory">Select Subcategory:</label>
      <select v-model="selectedSubcategory" @change="handleChange">
        <option v-for="subcategory in subcategories" :key="subcategory.id" :value="subcategory.id">{{ subcategory.name }}</option>
      </select>
    </div>
  </template>
  
  <script>
  import * as common from "../assets/common.js";
  export default {
    name:"Subcategory",
    props: ['value', 'category'], 
    data() {
      return {
        selectedSubcategory: this.value || '', 
        subcategories: [], 
      };
    },
    watch: {
      category(newValue) {
        this.fetchSubcategories(newValue);
      },
    },
    created() {
      this.fetchSubcategories(this.category);
    },
    methods: {
      fetchSubcategories(categoryId) {
        fetch(common.DISCOURSE_TICKET_API + '/category/subcategories/'+`${categoryId}`, {
            method: "GET",
            headers: {
              webtoken: this.$store.getters.get_web_token,
              userid: this.user_id,
            }
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.category == "success") {
                this.subcategories=data.message
                console.log("Sub categories are being rendered.")
                this.flashMessage.success({
                  message: "Sub categories retrived",
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
        this.$emit('input', this.selectedSubcategory);
      },
    },
  };
  </script>
  