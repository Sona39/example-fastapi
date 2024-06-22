<template>
  <div class="post-feed">
    <NotificationComponent v-if="notificationMessage" :message="notificationMessage" :type="notificationType" />
    <h2>Post Feed</h2>
    <div class="new-post-form">
      <h3>Create a New Post</h3>
      <form @submit.prevent="createPost">
        <div class="form-group">
          <label for="title">Title:</label>
          <input v-model="newPost.title" type="text" id="title" class="form-control" required />
        </div>
        <div class="form-group">
          <label for="content">Content:</label>
          <textarea v-model="newPost.content" id="content" class="form-control" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
    <div v-for="(post, index) in posts" :key="post.Post.id" class="post-item">
      <div class="post-header">
        <h3>{{ post.Post.title }}</h3>
        <div class="dropdown">
          <button class="dropbtn" @click="toggleDropdown(index)">...</button>
          <div class="dropdown-content" v-if="post.showDropdown">
            <a @click="updatePost(post.Post.id)">Update</a>
            <a @click="deletePost(post.Post.id)">Delete</a>
          </div>
        </div>
      </div>
      <div class="post-content">
        <p>{{ post.Post.content }}</p>
      </div>
      <div class="post-actions">
        <VoteComponent
          :postId="post.Post.id"
          :initialLikes="post.votes"
          :initialLiked="post.liked"
          @update:likes="updateLikes(index, $event)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import VoteComponent from './VoteComponent.vue';
import NotificationComponent from './NotificationComponent.vue';

export default {
  components: {
    VoteComponent,
    NotificationComponent
  },
  data() {
    return {
      posts: [],
      newPost: {
        title: '',
        content: ''
      },
      intervalId: null,
      notificationMessage: '',
      notificationType: ''
    };
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/posts');
        this.posts = response.data.map(post => ({
          ...post,
          showDropdown: false,
          liked: localStorage.getItem(`liked_${post.Post.id}`) === 'true' // Set liked state from local storage
        }));
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    },
    async createPost() {
      const token = localStorage.getItem('token');
      try {
        await axios.post('http://127.0.0.1:8000/posts', this.newPost, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.newPost.title = '';
        this.newPost.content = '';
        this.fetchPosts();
        this.showNotification('Post created successfully!', 'success');
      } catch (error) {
        console.error('Error creating post:', error);
        this.showNotification('Error creating post!', 'error');
      }
    },
    updatePost(id) {
      this.$router.push({ name: 'UpdatePost', params: { id } });
    },
    async deletePost(id) {
      const token = localStorage.getItem('token');
      try {
        await axios.delete(`http://127.0.0.1:8000/posts/${id}`, {
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
      }, 600000); // Refresh every 10 minutes (adjust as needed)
    },
    stopAutoRefresh() {
      clearInterval(this.intervalId);
    },
    showNotification(message, type) {
      this.notificationMessage = message;
      this.notificationType = type;
    },
    updateLikes(index, newLikes) {
      // Update the likes count for the post at the specified index
      this.posts[index].votes = newLikes;
    }
  },
  mounted() {
    this.fetchPosts();
    this.startAutoRefresh();
  },
  beforeUnmount() {
    this.stopAutoRefresh();
  }
};
</script>

<style scoped>
.post-feed {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color:#F9F8F0;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.new-post-form {
  background-color: #F0FFF0;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.new-post-form h3 {
  margin-top: 0;
  color: #333;
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
  background-color: #9CAF88;
  border-radius: 30px; /* Changed from 5px to 30px for rounded, pill-like shape */
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #8ca779;
}

.post-item {
  position: relative;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  padding: 20px;
  margin-bottom: 10px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.dropdown {
  position: relative;
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
  background-color: #fff;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  border-radius: 5px;
  display: block;
}

.dropdown-content a {
  color: #333;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  border-bottom: 1px solid #f1f1f1;
}

.dropdown-content a:hover {
  background-color: #f1f1f1;
}

.dropdown-content a:last-child {
  border-bottom: none;
}

.post-content {
  margin-right: 40px;
}

.post-actions {
  margin-top: auto;
  display: flex;
  justify-content: flex-end;
}

.votes {
  margin-top: 10px;
  color: #666;
}

.vote-component {
  margin-left: 10px;
}

.like-button {
  padding: 10px 20px; /* Increased padding for larger buttons */
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 30px; /* Changed from 5px to 30px for rounded, pill-like shape */
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.like-button:hover {
  background-color: #369870;
}

.like-button.liked {
  background-color: #f44336;
}

.like-button.liked:hover {
  background-color: #d32f2f;
}
</style>
