<template>
  <div class="update-post" v-if="post">
    <h2>Update Post</h2>
    <form @submit.prevent="updatePost">
      <div class="form-group">
        <label for="title">Title:</label>
        <input v-model="post.title" type="text" id="title" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="content">Content:</label>
        <textarea v-model="post.content" id="content" class="form-control" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Update</button>
    </form>
    <Notification v-if="notificationMessage" :message="notificationMessage" :type="notificationType" />
  </div>
</template>

<script>
import axios from 'axios';
import Notification from './NotificationComponent.vue';

export default {
  components: {
    Notification,
  },
  data() {
    return {
      post: null,
      notificationMessage: '', // Add this line
      notificationType: 'success', // Add this line
    };
  },
  methods: {
    async fetchPost(id) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/posts/${id}`);
        this.post = response.data.Post;
      } catch (error) {
        console.error('Error fetching post:', error);
        // Optionally handle errors or set a default state for `this.post`
      }
    },
    async updatePost() {
      try {
        await axios.put(`http://127.0.0.1:8000/posts/${this.$route.params.id}`, this.post, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`, // Assuming token is stored in localStorage
          },
        });
        // Set notification message and type
        this.notificationMessage = 'Post updated successfully!';
        this.notificationType = 'success';
        // Optionally navigate to the PostFeed page after a delay
        setTimeout(() => {
          this.notificationMessage = ''; // Clear the message
          this.$router.push({ name: 'PostFeed' });
        }, 2000);
      } catch (error) {
        console.error('Error updating post:', error);
        // Set notification message and type for error
        this.notificationMessage = 'Error updating post! You are not the owner of this post';
        this.notificationType = 'error';
      }
    },
  },
  async mounted() {
    const postId = this.$route.params.id;
    await this.fetchPost(postId);
  },
};
</script>

<style scoped>
.update-post {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  text-decoration: none;
  color: #fff;
  background-color: #42b983;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: #369870;
}
</style>
