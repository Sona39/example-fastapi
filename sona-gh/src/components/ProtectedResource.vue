<template>
    <div>
      <h1>Protected Resource</h1>
      <p>{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from '../axios'; 
  
  export default {
    name: 'ProtectedResource',
    data() {
      return {
        message: ''
      };
    },
    async created() {
      try {
        const response = await axios.get('/protected-resource/');
        this.message = response.data.message;
      } catch (err) {
        this.message = 'Error fetching protected resource';
      }
    }
  };
  </script>
  
  <style scoped>
  </style>
  







