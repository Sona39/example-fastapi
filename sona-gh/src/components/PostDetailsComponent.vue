<template>
  <div class="post-details" v-if="post">
    <h2>{{ post.Post.title }}</h2>
    <p>{{ post.Post.content }}</p>
    <p><strong>Votes: </strong>{{ post.votes }}</p>
    <button @click="vote(post.Post.id)">Vote</button>
    <button @click="editPost(post.Post.id)">Edit</button>
  </div>
</template>

<script>
import axiosInstance from '../axios';

export default {
  data() {
    return {
      post: null,
    };
  },
  methods: {
    async fetchPost(id) {
      const response = await axiosInstance.get(`/posts/${id}`);
      this.post = response.data;
    },
    async vote(id) {
      await axiosInstance.post(`/vote/${id}`);
      this.fetchPost(id);
    },
    editPost(id) {
      this.$router.push({ name: 'UpdatePost', params: { id } });
    },
  },
  mounted() {
    const postId = this.$route.params.id;
    this.fetchPost(postId);
  },
};
</script>

<style scoped>
.post-details {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}
</style>