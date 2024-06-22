<template>
  <div class="vote-component">
    <button @click="toggleLike" :class="{ 'liked': liked }" class="like-button">
      <i :class="['heart-icon', liked ? 'fas fa-heart' : 'far fa-heart']"></i>
      <span>{{ likes }}</span>
    </button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    postId: Number,
    initialLikes: {
      type: Number,
      default: 0
    },
    initialLiked: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      likes: this.initialLikes,
      liked: this.initialLiked
    };
  },
  mounted() {
    this.likes = this.initialLikes;
    this.liked = this.initialLiked;
  },
  methods: {
    async toggleLike() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post(`http://127.0.0.1:8000/vote/${this.postId}`, {
          liked: !this.liked
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.likes = response.data.likes; // Update local likes count
        this.liked = !this.liked;

        // Emit event to notify parent component of updated likes count
        this.$emit('update:likes', this.likes);
      } catch (error) {
        console.error('Error toggling like:', error);
      }
    }
  }
};
</script>

<style scoped>
.like-button {
  display: flex;
  align-items: center;
  background-color: transparent;
  border: none;
  cursor: pointer;
  outline: none;
}

.heart-icon {
  font-size: 24px;
  margin-right: 5px;
}

.fas.fa-heart {
  color: #f44336; /* Filled heart color */
}

.far.fa-heart {
  color: #aaa; /* Outline heart color */
}

.like-button span {
  font-size: 14px;
  color: #333;
  margin-left: 5px;
}

.like-button:hover .fas.fa-heart {
  color: #d32f2f; /* Filled heart color on hover */
}

.like-button:hover .far.fa-heart {
  color: #666; /* Outline heart color on hover */
}
</style>