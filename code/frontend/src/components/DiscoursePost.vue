<template>
    <div class="post">
      <h3>{{ post.name }}</h3>
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
  