<template>
    <div class="post">
      <b-icon
                    icon="person-fill"
                    aria-hidden="true"
                    class="bg-light"
                    variant="danger"
                  ></b-icon><h5>{{ post.name }}</h5>
      <div v-html="post.cooked"></div>
    </div>
  </template>
  
  <script>
  export default {
    name:"Post",
    props: {
      post: {
        type: Object,
        required: true
      }
    }
  };
  </script>
  
  <style scoped>
  .post {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 20px;
  }
  </style>
  