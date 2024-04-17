<template>
    <div>
      <h2>Subcategories</h2>
      <div v-for="subcategory in subcategories" :key="subcategory.id">
        <p>{{ subcategory.name }}</p>
      </div>
      <form @submit="createSubcategory" class="ticket-form" style="margin-top: 5px; margin-left: 5px; margin-right: 5px; text-align: left">
        <div>
          <label for="name">Subcategory Name:</label>
          <input type="text" id="name" v-model="form.name" required>
        </div>
        <div>
          <label for="color">Color:</label>
          <input type="color" id="color" v-model="form.color">
          <span>{{ selectedColorHex }}</span>
        </div>
        <div>
          <label for="color">Text Color:</label>
          <input type="color" id="color" v-model="form.text_color">
          <span>{{ selectedTextColorHex }}</span>
        </div>
        <div>
          <label for="description">Description:</label>
          <textarea id="description" v-model="form.description"></textarea>
        </div>
        <b-button type="submit" variant="primary" @click="createSubcategory">Create Subcategory</b-button>
      </form>
    </div>
  </template>
  
  <script>
  import * as common from "../assets/common.js";
  
  export default {
    name:"CreateSubcategory",
    components: {
    },
    data() {
      return {
        subcategories: [],
        form: {
          name: '',
          color: '',
          description: '',
          text_color:'',
        },
        selectedColor: '#000000',
        selectedTextColor:"#000000"
      };
    },
    computed: {
      selectedColorHex() {
        return this.selectedColor.toUpperCase();
      },
      selectedTextColorHex()
      {
        return this.selectedTextColor.toUpperCase();
      }
    },
    mounted() {
      this.fetchSubcategories();
    },
    methods: {
      fetchSubcategories() {
        fetch(common.DISCOURSE_TICKET_API + '/category/subcategories/14', {
            method: "GET",
            headers: {
              webtoken: this.$store.getters.get_web_token,
              userid: this.user_id,
            }
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.category == "success") {
                this.subcategories=data.message;
                console.log("Sub categories are being rendered.");
                console.log(this.subcategories);
                this.onReset();
              }
              if (data.category == "error") {
                console.log("cannot retrieve sub categories.")
              }
            })
            .catch((error) => {
              this.$log.error(`Error : ${error}`);
              console.log("Sub categories cannot be retrieved.")
            });
      },
      createSubcategory() {
        this.newSubcategory.color = this.selectedColorHex;
        
        fetch(common.DISCOURSE_TICKET_API + '/category', {
          method: "POST",
          headers: {
            webtoken: this.$store.getters.get_web_token,
            userid: this.$store.getters.get_user_id,
          },
          body: JSON.stringify(this.form),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.category == "success") {
              this.flashMessage.success({
                message: data.message,
              });
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
    }
  };
  </script>
  