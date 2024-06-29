<template>
  <div class="create-post">
    <h2>Create Post</h2>
    <form @submit.prevent="createPost">
      <div class="form-group">
        <label for="title" class="label">Title:</label>
        <input v-model="form.title" type="text" id="title" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="content" class="label">Content:</label>
        <textarea v-model="form.content" id="content" class="form-control" rows="5" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Create Post</button>
    </form>
    <Notification v-if="notificationMessage" :message="notificationMessage" :type="notificationType" />
  </div>
</template>

<script>
import axiosInstance from '../axios';
import Notification from './NotificationComponent.vue';

export default {
  data() {
    return {
      form: {
        title: '',
        content: ''
      },
      notificationMessage: '',
      notificationType: 'success'
    };
  },
  methods: {
    async createPost() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('No token available');
        }

        await axiosInstance.post('/posts/', this.form, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        this.form.title = '';
        this.form.content = '';

        this.notificationMessage = 'Post created successfully!';
        this.notificationType = 'success';

        this.$emit('postCreated');

      } catch (error) {
        console.error('Error creating post:', error);

        this.notificationMessage = 'Error creating post!';
        this.notificationType = 'error';
      }
    }
  },
  components: {
    Notification
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap');

.create-post {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fefefc;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the container */
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the heading */
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to labels */
}

.form-control {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to inputs */
}

.btn {
  display: inline-block;
  padding: 10px 20px; /* Adjusted padding for better touch area */
  font-size: 14px; /* Kept the font size */
  font-weight: bold;
  text-align: center;
  text-decoration: none;
  color: #fff;
  background-color: #9caf88;
  border-radius: 30px; /* Kept the rounded, pill-like shape */
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the button */
}

.btn:hover {
  background-color: #5F4F4D;
}
</style>
