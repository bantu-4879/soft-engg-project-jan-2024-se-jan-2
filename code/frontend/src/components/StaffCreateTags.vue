<template>
    <div>
      <h4>Tags</h4>
      <div v-for="tag in tags" :key="tag.id">
        <p>{{ tag.name }}</p>
      </div>
      <b-form @submit="createTag()" class="tags-form" style="margin-top: 5px; margin-left: 5px; margin-right: 5px; text-align: center;width: 250px; border-left: 10px;">
        <b-form-group label="Tag Name:" label-for="tag-name">
          <b-form-input v-model="tagName" id="tag-name" type="text" required></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Create Tag</b-button>
      </b-form>
    </div>
  </template>
  
  <script>
    import * as common from "../assets/common.js";
  export default {
    name:"CreateTags",
    data() {
      return {
        tags: [],
        tagName: '',
        user_id:this.$store.getters.get_user_id
      };
    },
    mounted() {
      this.fetchTags();
    },
    methods: {
      fetchTags() {
        fetch(common.DISCOURSE_TICKET_API+'/tags',{
            method: "GET",
            headers: {
              webtoken: this.$store.getters.get_web_token,
              userid: this.user_id,
            }
          })
          .then(response => {
            if (!response.ok) {
              throw new Error('Failed to fetch tags');
            }
            return response.json();
          })
          .then(data => {
            this.tags = data.message;
          })
          .catch(error => {
            console.error('Error fetching tags:', error);
          });
      },
      createTag() {
        if (!this.tagName.trim()) {
            this.flashMessage.error({
              message: "Tag name cannot be empty.",
            });
        return;
      }
      const data = {
        tags: [this.tagName]
      };
        fetch(common.DISCOURSE_TICKET_API+'/tags', {
          method: 'POST',
          headers: {
            webtoken: this.$store.getters.get_web_token,
            userid: this.user_id,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to create tag');
          }
          return response.json();
        })
        .then(data => {
          this.fetchTags();
          this.tagName = ''; 
          this.flashMessage.success({
                message: data.message,
              });
        })
        .catch(error => {
          console.error('Error creating tag:', error);
          this.flashMessage.error({
              message: error.message,
            });
        });
      },
    },
  };
  </script>
  