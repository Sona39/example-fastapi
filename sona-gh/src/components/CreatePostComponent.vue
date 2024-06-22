<template>
  <div class="create-post">
    <h2>Create Post</h2>
    <form @submit.prevent="createPost">
      <div>
        <label for="title">Title:</label>
        <input v-model="form.title" type="text" id="title" required />
      </div>
      <div>
        <label for="content">Content:</label>
        <textarea v-model="form.content" id="content" required></textarea>
      </div>
      <button type="submit">Create</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        title: '',
        content: '',
      },
    };
  },
  methods: {
    async createPost() {
      await axios.post('http://127.0.0.1:8000/posts', this.form);
      this.$router.push({ name: 'PostFeed' });
    },
  },
};
</script>

<style scoped>
.create-post {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}
</style>