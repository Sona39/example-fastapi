<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="registerUser">
      <div class="form-group">
        <label for="first_name">First Name:</label>
        <input v-model.trim="form.first_name" type="text" id="first_name" required @blur="validateName('first_name')" />
        <span v-if="!isInitialFirstNameValid && !form.first_name" class="initial-error-message">First Name is required.</span>
        <span v-if="!isInitialFirstNameValid && form.first_name && !isValidName('first_name')" class="error-message">Please enter only letters.</span>
      </div>
      <div class="form-group">
        <label for="last_name">Last Name:</label>
        <input v-model.trim="form.last_name" type="text" id="last_name" required @blur="validateName('last_name')" />
        <span v-if="!isInitialLastNameValid && !form.last_name" class="initial-error-message">Last Name is required.</span>
        <span v-if="!isInitialLastNameValid && form.last_name && !isValidName('last_name')" class="error-message">Please enter only letters.</span>
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input v-model.trim="form.email" type="email" id="email" required @blur="validateEmail" />
        <span v-if="!isInitialEmailValid && !form.email" class="initial-error-message">Email is required.</span>
        <span v-if="!isInitialEmailValid && form.email && !isValidEmail" class="error-message">Please enter a valid email address.</span>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <div class="password-input-container">
          <input v-model="form.password" :type="passwordFieldType" id="password" required @blur="validatePassword" />
          <div class="password-toggle" @mousedown.prevent>
            <i class="fas" :class="passwordFieldType === 'password' ? 'fa-eye-slash' : 'fa-eye'" @click="togglePasswordVisibility"></i>
          </div>
        </div>
        <span v-if="!isInitialPasswordValid && !form.password" class="initial-error-message">Password is required.</span>
        <span v-if="!isInitialPasswordValid && form.password && !isValidPassword" class="error-message">
          Password must be at least 8 characters long, contain at least one uppercase letter, one number, and one special character.
        </span>
      </div>
      <button type="submit" :disabled="!isValidForm">Register</button>
    </form>
  </div>
</template>

<script>
import axiosInstance from '../axios';


export default {
  data() {
    return {
      form: {
        email: '',
        password: '',
        first_name: '',
        last_name: ''
      },
      isInitialEmailValid: true,
      isInitialPasswordValid: true,
      isInitialFirstNameValid: true,
      isInitialLastNameValid: true,
      passwordFieldType: 'password' // Initial type of password input
    };
  },
  computed: {
    isValidEmail() {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailPattern.test(this.form.email);
    },
    isValidPassword() {
      const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      return passwordPattern.test(this.form.password);
    },
    isValidForm() {
      return this.isValidEmail && this.isValidPassword && this.isValidName('first_name') && this.isValidName('last_name');
    }
  },
  methods: {
    validateEmail() {
      this.isInitialEmailValid = false;
    },
    validatePassword() {
      this.isInitialPasswordValid = false;
    },
    validateName(field) {
      if (field === 'first_name') {
        this.isInitialFirstNameValid = false;
      } else if (field === 'last_name') {
        this.isInitialLastNameValid = false;
      }
    },
    isValidName(field) {
      const namePattern = /^[A-Za-z]+$/;
      if (field === 'first_name') {
        return namePattern.test(this.form.first_name);
      } else if (field === 'last_name') {
        return namePattern.test(this.form.last_name);
      }
      return false;
    },
    togglePasswordVisibility() {
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
    },
    async registerUser() {
      if (this.isValidForm) {
        try {
          const response = await axiosInstance.post('/users', {
            email: this.form.email,
            password: this.form.password,
            first_name: this.form.first_name,
            last_name: this.form.last_name
          });
          console.log(response.data);
          // Navigate to login page upon successful registration
          this.$router.push('/login');
        } catch (error) {
          console.error(error);
          // Handle registration error, such as displaying an error message
        }
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap');

.register-container {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #9CAF88;
  border-radius: 5px;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the container */
}

h2 {
  text-align: center;
  color: #5F4F4D;
  margin-bottom: 20px;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the heading */
}

form {
  display: flex;
  flex-direction: column;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the form */
}

.form-group {
  margin-bottom: 15px;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the form group */
}

label {
  display: block;
  margin-bottom: 5px;
  color: #5F4F4D;
  font-weight: bold;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the label */
}

input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s ease;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the input */
}

input:focus {
  outline: none;
  border-color: #9CAF88;
}

.password-input-container {
  position: relative;
}

.password-input-container input {
  padding-right: 40px;
}

.password-toggle {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #5F4F4D;
}

button[type="submit"] {
  padding: 12px 24px;
  background-color: #9CAF88;
  color: white;
  border: 2px solid #9CAF88;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  text-align: center;
  text-transform: uppercase;
  transition: background-color 0.3s ease, border-color 0.3s ease;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the button */
}

button[type="submit"]:hover {
  background-color: #5F4F4D;
  border-color: #5F4F4D;
}

button[type="submit"]:disabled {
  background-color: #ccc;
  border-color: #ccc;
  cursor: not-allowed;
}

.error-message,
.initial-error-message {
  color: #f00;
  font-size: 0.85rem;
  text-align: center;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to the error messages */
}
</style>
