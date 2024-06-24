<template>
  <div class="create-post-container">
    <CreatePostComponent @postCreated="handlePostCreated" />
  </div>

  <div class="post-feed">
    <NotificationComponent v-if="notificationMessage" :message="notificationMessage" :type="notificationType" />

    <h2>Post Feed</h2>

    <div v-for="(post, index) in posts" :key="post.Post.id" class="post-item">
      <div v-if="post.Post.owner" class="post-owner-info">
        <span class="owner-name">{{ post.Post.owner.first_name }} {{ post.Post.owner.last_name }}</span>
      </div>

      <div v-if="isOwner(post.Post.owner.id)" class="dropdown">
        <button class="dropbtn" @click="toggleDropdown(index)">...</button>
        <div class="dropdown-content" v-if="post.showDropdown">
          <a @click="updatePost(post.Post.id)">Update</a>
          <a @click="deletePost(post.Post.id)">Delete</a>
        </div>
      </div>

      <div class="post-header">
        <h3>{{ post.Post.title }}</h3>
      </div>
      <div class="post-content">
        <p>{{ post.Post.content }}</p>
      </div>
      <div class="post-actions">
        <VoteComponent
          :postId="post.Post.id"
          :initialLikes="post.votes"
          @update:likes="updateLikes(index, $event)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import CreatePostComponent from './CreatePostComponent.vue';
import VoteComponent from './VoteComponent.vue';
import NotificationComponent from './NotificationComponent.vue';
import axiosInstance from '../axios';



export default {
  components: {
    CreatePostComponent,
    VoteComponent,
    NotificationComponent
  },
  data() {
    return {
      posts: [],
      notificationMessage: '',
      notificationType: '',
      userId: null,
      apiHost: process.env.API_HOST,
      apiPort: process.env.API_PORT
    };
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await axiosInstance.get(`/posts/`);

        this.posts = response.data.map(post => ({
          ...post,
          showDropdown: false
        }));
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    },
    async updatePost(id) {
      this.$router.push({ name: 'UpdatePost', params: { id } });
    },
    async deletePost(id) {
      const token = localStorage.getItem('token');
      try {
        await axiosInstance.delete(`/posts/${id}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.fetchPosts();
        this.showNotification('Post deleted successfully!', 'success');
      } catch (error) {
        console.error('Error deleting post:', error);
        this.showNotification('Error deleting post!', 'error');
      }
    },
    toggleDropdown(index) {
      this.posts = this.posts.map((post, i) => ({
        ...post,
        showDropdown: i === index ? !post.showDropdown : false
      }));
    },
    startAutoRefresh() {
      this.intervalId = setInterval(() => {
        this.fetchPosts();
      }, 60000);
    },
    stopAutoRefresh() {
      clearInterval(this.intervalId);
    },
    showNotification(message, type) {
      this.notificationMessage = message;
      this.notificationType = type;
    },
    updateLikes(index, newLikes) {
      this.posts[index].votes = newLikes;
    },
    handlePostCreated() {
      this.fetchPosts();
    },
    isOwner(ownerId) {
      return this.userId === ownerId;
    }
  },
  mounted() {
    this.fetchPosts();
    this.startAutoRefresh();
    const token = localStorage.getItem('token');
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      this.userId = payload.user_id;
    }
  },
  beforeUnmount() {
    this.stopAutoRefresh();
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap');

.post-feed {
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

.new-post-form {
  background-color: #f9f8f0;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.new-post-form h3 {
  margin-top: 0;
  color: #333;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the subheading */
}

.form-group {
  margin-bottom: 15px;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the form group */
}

.form-control {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the form control */
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
  background-color: #8ca779;
}

.post-item {
  position: relative;
  background-color: #f9f8f0;
  border: 1px solid #ccc;
  padding: 20px;
  margin-bottom: 10px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the post item */
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.post-header h3 {
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the post title */
}

.dropdown {
  position: absolute;
  top: 10px; /* Adjust as needed */
  right: 10px; /* Adjust as needed */
}

button.dropbtn {
  background-color: transparent;
  color: #333;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.dropdown-content {
  position: absolute;
  right: 0;
  min-width: 160px;
  box-shadow: #fff;
  background-color:  #9CAF88; /* Button background color */
  color: #fff; /* Button text color */
  cursor: pointer;
  border-radius: 20px;
  transition: background-color 0.3s ease;
  z-index: 1;
  border-radius: 10px;
  display: none;
}

.dropdown:hover .dropdown-content {
  display: block;
}

.dropdown-content a {
  color:#fff;
  padding: 12px 16px;
  text-decoration: none;
  color: #fff;
  display: block;
  border-bottom: 1px solid #f1f1f1;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the dropdown items */
}

.dropdown-content a:hover {
  background-color: #5F4F4D; /* Button background color on hover */
  color:#fff;
}

.dropdown-content a:last-child {
  border-bottom: none;
}

.post-content {
  margin-right: 40px;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the post content */
}

.post-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-top: auto;
}

.votes {
  margin-top: 10px;
  color: #666;
}

.vote-component {
  margin-left: 10px;
}

.like-button {
  padding: 10px 20px;
  background-color: #9caf88;
  color: white;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the like button */
}

.like-button:hover {
  background-color: #8ca779;
}

.like-button.liked {
  background-color: #8ca779;
}

.like-button.liked:hover {
  background-color: #d32f2f;
}

.owner-name {
  font-size: 14px;
  color: #666;
  font-weight: bold;
  margin-bottom: 5px;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the owner name */
}
</style>
