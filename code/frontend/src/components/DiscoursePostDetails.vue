<template>
    <div class="post-details">
      <h1>{{ message.title }}</h1>
      <b-icon
                    icon="chat-right-quote-fill"
                    aria-hidden="true"
                    class="bg-light"
                    variant="danger"
                  ></b-icon><h6>{{ message.post_counts }} </h6>
      <PostStream :posts="message.post_stream.posts" />
                  <b-icon
                    icon="heart-fill"
                    aria-hidden="true"
                    class="bg-light"
                    variant="danger"
                  ></b-icon><h6>{{ message.like_count }} </h6>
    </div>
  </template>
  
  <script>
  import PostStream from './DiscoursePostStream.vue';
  
  export default {
    name:"PostDetail",
    props: {
      message: {
        type: Object,
        required: true
      }
    },
    components: {
      PostStream,
    }
  };
  </script>
  
  <style scoped>
  .post-details {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .post-details h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  </style>
  