<template>
    <div>
      <h4>Subcategories</h4>
      <div v-for="subcategory in subcategories" :key="subcategory.id">
        <p>{{ subcategory.name }}</p>
      </div>
      <b-form @submit="createSubcategory()" class="ticket-form" style="margin-top: 5px; margin-left: 5px; margin-right: 5px; text-align: center;width: 300px; border-left: 10px;">
    <b-form-group label="Subcategory Name:" label-for="name">
        <b-form-input id="name" v-model="form.name" type="text" required></b-form-input>
    </b-form-group>
    <b-form-group label="Color:" label-for="color">
        <b-form-input id="color" v-model="form.color" type="color"></b-form-input>
        <span>{{ selectedColorHex }}</span>
    </b-form-group>
    <b-form-group label="Text Color:" label-for="text-color">
        <b-form-input id="text-color" v-model="form.text_color" type="color"></b-form-input>
        <span>{{ selectedTextColorHex }}</span>
    </b-form-group>
    <b-form-group label="Description:" label-for="description">
        <b-form-textarea id="description" v-model="form.description"></b-form-textarea>
    </b-form-group>
    <b-button type="submit" variant="primary">Create Subcategory</b-button>
</b-form>
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

        this.form.color.color = this.selectedColorHex;
        this.form.text_color=this.selectedTextColorHex;
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
  