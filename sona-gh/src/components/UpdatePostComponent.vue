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
import axiosInstance from '../axios';
import Notification from './NotificationComponent.vue';

export default {
  components: {
    Notification,
  },
  data() {
    return {
      post: null,
      notificationMessage: '',
      notificationType: 'success',
    };
  },
  methods: {
    async fetchPost(id) {
      try {
        const response = await axiosInstance.get(`/posts/${id}`);
        this.post = response.data.Post;
      } catch (error) {
        console.error('Error fetching post:', error);
        // Optionally handle errors or set a default state for `this.post`
      }
    },
    async updatePost() {
      try {
        await axiosInstance.put(`/posts/${this.$route.params.id}`, this.post, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        // Set notification message and type
        this.notificationMessage = 'Post updated successfully!';
        this.notificationType = 'success';
        // Optionally navigate to the PostFeed page after a delay
        setTimeout(() => {
          this.notificationMessage = '';
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
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

.update-post {
  font-family: 'Montserrat', sans-serif;
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
  font-family: 'Montserrat', sans-serif;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  font-family: 'Montserrat', sans-serif;
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.btn {
  display: inline-block;
  padding: 12px 24px; /* Adjusted padding */
  font-size: 14px;
  font-weight: bold;
  font-family: 'Montserrat', sans-serif;
  text-align: center;
  text-decoration: none;
  color: white;
  background-color: #9CAF88; /* Ecru White */
  border: 2px solid #9CAF88; /* Ecru White */
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.btn:hover {
  background-color: #5F4F4D; /* Martini */
  border-color: #5F4F4D; /* Martini */
}
</style>
