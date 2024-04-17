
<template>
  <div>
    <label for="category">Select Category:</label>
    <b-dropdown v-model="selectedCategory" id="dropdown-cats">
      <template #button-content>
        <b-icon icon="lock-fill" aria-hidden="true"></b-icon> 
        {{ getCategoryName(selectedCategory) }}
      </template>
      <b-dropdown-item v-for="category in categories" :key="category.id" :value="category.id" @click="handleChange(category.id)">
        {{ category.name }}
      </b-dropdown-item>
    </b-dropdown>
  </div>
</template>
  
  <script>
  import * as common from "../assets/common.js";
  
  export default {
    name:"Category", 
    data() {
      return {
        selectedCategory: 14 || '', 
        categories: [], 
        lockedCategoryId:14,
        user_id:this.$store.getters.get_user_id,
      };
    },
    created() {
      this.fetchCategories();
    },
    methods: {
      getCategoryName(categoryId) {
    const category = this.categories.find(cat => cat.id === categoryId);
    return category ? category.name : 'Select Category';
  },
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
                this.onReset();
              }
              if (data.category == "error") {

                console.log("cannot retrieve categories.")
              }
            })
            .catch((error) => {
              this.$log.error(`Error : ${error}`);
              console.log("cannot retrieve categories.");
            });

      },
      handleChange() {
        this.$emit('input', this.selectedCategory);
      },
    },
  };
  </script>
  