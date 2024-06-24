<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required @input="validateEmail" />
        <span v-if="!isValidEmail && isEmailTouched" class="error-message">Please enter a valid email address.</span>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <div class="password-input-container">
          <input
            :type="passwordFieldType"
            id="password"
            v-model="password"
            required
            @input="validatePassword"
            :class="{ 'error': !isValidPassword && isPasswordTouched }"
          />
          <span class="toggle-password" @click="togglePasswordVisibility">
            <i :class="passwordFieldType === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
          </span>
        </div>
        <span v-if="!isValidPassword && isPasswordTouched" class="error-message">
          Password must be at least 8 characters long, contain at least one uppercase letter, one number, and one special character.
        </span>
      </div>
      <button type="submit" :disabled="!isValidForm" class="btn btn-login">Login</button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import axios from '../axios'; // Assuming you have a custom axios instance

export default {
  name: 'LoginComponent',
  data() {
    return {
      email: '',
      password: '',
      error: null,
      isEmailValid: true,
      isPasswordValid: true,
      isEmailTouched: false,
      isPasswordTouched: false,
      passwordFieldType: 'password' // Initial type of password input
    };
  },
  computed: {
    isValidEmail() {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return this.isEmailTouched ? emailPattern.test(this.email) : true;
    },
    isValidPassword() {
      const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      return this.isPasswordTouched ? passwordPattern.test(this.password) : true;
    },
    isValidForm() {
      return this.isValidEmail && this.isValidPassword;
    }
  },
  methods: {
    validateEmail() {
      this.isEmailTouched = true;
    },
    validatePassword() {
      this.isPasswordTouched = true;
    },
    togglePasswordVisibility() {
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
    },
    async login() {
      try {
        const formData = new FormData();
        formData.append('username', this.email);
        formData.append('password', this.password);

        const response = await axios.post('/login/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        localStorage.setItem('token', response.data.access_token);
        this.$router.push('/');
      } catch (err) {
        this.error = 'Invalid email or password';
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #9CAF88; /* Ecru White */
  border-radius: 5px;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Adding subtle shadow for depth */
}

h2 {
  text-align: center;
  color: #5F4F4D; /* Martini */
  margin-bottom: 20px; /* Increased spacing between heading and form */
}

form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px; /* Increased spacing between form groups */
}

label {
  display: block;
  margin-bottom: 5px;
  color: #5F4F4D; /* Martini */
  font-weight: bold; /* Added bold font weight for labels */
}

input {
  width: 100%;
  padding: 10px; /* Increased input padding for better touch target */
  box-sizing: border-box;
  border: 1px solid #ccc; /* Light gray border */
  border-radius: 5px;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #9CAF88; /* Ecru White on focus */
}

.password-input-container {
  position: relative;
}

.password-input-container input {
  padding-right: 40px; /* Space for the eye icon */
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #5F4F4D; /* Martini */
}

.btn {
  display: inline-block;
  padding: 12px 24px; /* Increased padding for button */
  font-size: 14px; /* Default font size */
  font-weight: bold;
  text-align: center;
  text-decoration: none;
  color: #fff;
  background-color: #9CAF88; /* Ecru White */
  border: 2px solid #9CAF88; /* Ecru White */
  border-radius: 20px;
  cursor: pointer;
  text-transform: uppercase;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.btn-login:hover {
  background-color: #5F4F4D; /* Martini on hover */
  border-color: #5F4F4D; /* Martini on hover */
}

.btn-login:disabled {
  background-color: #ccc;
  border-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #f00;
  font-size: 0.85rem;
  margin-top: 8px; /* Increased top margin for error message */
  text-align: center; /* Centered error message */
}
</style>
