<template>
  <header class="header">
    <nav class="navbar">
      <div class="navbar-brand">
        <router-link to="/">
          <img src="../assets/logo.png" alt="Ferny" class="logo" />
        </router-link>
      </div>
      <div class="navbar-menu">
        <router-link v-if="isLoggedIn" to="/account" class="navbar-item">{{ userName }}</router-link>
        <router-link v-if="!isLoggedIn" to="/login" class="navbar-item btn">Login</router-link>
        <router-link v-if="!isLoggedIn" to="/register" class="navbar-item btn">Register</router-link>
        <button v-if="isLoggedIn" @click="logout" class="navbar-item btn-logout">Log Out</button>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: "HeaderComponent",
  data() {
    return {
      isLoggedIn: false,
      userEmail: '',
      userName: '' // To store user's full name
    };
  },
  mounted() {
    this.checkAuthentication();
  },
  watch: {
    '$route': 'checkAuthentication'
  },
  methods: {
    checkAuthentication() {
      const token = localStorage.getItem('token');
      if (token) {
        const decodedToken = JSON.parse(atob(token.split('.')[1]));
        this.isLoggedIn = true;
        this.userEmail = decodedToken.email; // Assuming email is stored in the token
        this.userName = `${decodedToken.first_name} ${decodedToken.last_name}`;
      } else {
        this.isLoggedIn = false;
        this.userEmail = '';
        this.userName = '';
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.isLoggedIn = false;
      this.userEmail = '';
      this.userName = '';
      this.$router.push('/login'); // Redirect to login page after logout
    }
  }
};
</script>

<style scoped>
.header {
  background-color: #9CAF88; /* Ecru White */
  padding: 10px 0;
}

.navbar {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.navbar-brand {
  grid-column: 2;
  display: flex;
  justify-content: center;
}

.navbar-brand .logo {
  height: 150px;
}

.navbar-menu {
  grid-column: 3;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.navbar-item {
  margin: 0 10px;
  color: #5F4F4D; /* Martini */
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.navbar-item:hover {
  text-decoration: underline;
  color: #5F4F4D; /* Tan */
}

.btn {
  padding: 10px 20px;
  border: 2px solid #5F4F4D; /* Use the existing color */
  border-radius: 20px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  text-align: center;
  text-transform: uppercase;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.btn-logout {
  padding: 10px 20px;
  border: 2px solid #5F4F4D; /* Use the existing color */
  border-radius: 30px;
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
  text-align: center;
  text-transform: uppercase;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.btn:hover,
.btn-logout:hover {
  border-color: #5F4F4D ; /* Martini */
}
</style>
