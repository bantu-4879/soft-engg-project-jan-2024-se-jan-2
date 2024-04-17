<template>
    <div>
      <Post v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </template>
  
  <script>
  import Post from './DiscoursePost.vue';
  
  export default {
    name:"PostStream",
    props: {
      posts: {
        type: Array,
        required: true
      }
    },
    components: {
      Post
    }
  };
  </script>
  