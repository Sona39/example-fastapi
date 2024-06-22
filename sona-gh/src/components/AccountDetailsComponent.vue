<template>
  <div class="account-details">
    <h1>Account Details</h1>
    <span @click="openReauthModal" class="edit-icon"></span>
    <div class="user-info" :class="{ 'disabled': !isEditable }">
      <div class="info-item">
        <label class="label">Email:</label>
        <input type="email" v-model="userEmail" class="input" :disabled="!isEditable" />
        <button v-if="isEditable" @click="saveEmailChanges" class="btn-save">Save Email</button>
      </div>
      <div class="info-item">
        <label class="label">First Name:</label>
        <input type="text" v-model="firstName" class="input" :disabled="!isEditable" />
        <button v-if="isEditable" @click="saveFirstNameChanges" class="btn-save">Save First Name</button>
      </div>
      <div class="info-item">
        <label class="label">Last Name:</label>
        <input type="text" v-model="lastName" class="input" :disabled="!isEditable" />
        <button v-if="isEditable" @click="saveLastNameChanges" class="btn-save">Save Last Name</button>
      </div>
      <div class="info-item" v-if="showNewPassword">
        <label class="label">New Password:</label>
        <input type="password" v-model="newPassword" class="input" :disabled="!isEditable" />
        <button v-if="isEditable" @click="savePasswordChange" class="btn-save">Save Password</button>
      </div>
    </div>

    <div v-if="successMessage" class="notification success">
      <p>Data was changed successfully!</p>
    </div>

    <div v-if="showReauthModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeReauthModal">&times;</span>
        <h2>Re-authenticate</h2>
        <input type="password" v-model="reauthPassword" placeholder="Enter your password" class="input" />
        <button @click="reauthenticate" class="btn-save">Submit</button>
        <p v-if="reauthError" class="error-msg">{{ reauthError }}</p> <!-- Password is incorrect -->
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../axios'; // Adjust the path as needed

export default {
  name: "AccountDetails",
  data() {
    return {
      userEmail: "",
      firstName: "",
      lastName: "",
      newPassword: "",
      successMessage: false,
      isEditable: false,
      showReauthModal: false,
      showNewPassword: false,
      reauthPassword: "",
      reauthError: "" // Initialize reauthError for error handling
    };
  },
  mounted() {
    this.getUserDetails();
  },
  methods: {
    getUserDetails() {
      const token = localStorage.getItem("token");
      if (token) {
        const decodedToken = JSON.parse(atob(token.split(".")[1]));
        this.userEmail = decodedToken.user_email;
        this.firstName = decodedToken.first_name;
        this.lastName = decodedToken.last_name;
      }
    },
    openReauthModal() {
      this.showReauthModal = true;
    },
    closeReauthModal() {
      this.showReauthModal = false;
      this.reauthPassword = "";
      this.reauthError = ""; // Reset reauthError when closing modal
    },
    async reauthenticate() {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Token not found. Please login again.");
        return;
      }

      const decodedToken = JSON.parse(atob(token.split(".")[1]));
      const username = decodedToken.user_email; // Assuming user_email is the username
      const password = this.reauthPassword;

      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      try {
        const response = await axiosInstance.post('/login', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        if (response.status === 200){
          this.isEditable = true;
          this.showNewPassword = true;
          this.closeReauthModal();
        }
      } catch (error) {
        console.error("Re-authentication failed:", error);
        this.reauthError = "Incorrect password. Please try again."; // Set error message
      }
    },
    async saveEmailChanges() {
      // Implement email update logic here
      await this.saveFieldChanges('email', this.userEmail);
    },
    async saveFirstNameChanges() {
      // Implement first name update logic here
      await this.saveFieldChanges('first_name', this.firstName);
    },
    async saveLastNameChanges() {
      // Implement last name update logic here
      await this.saveFieldChanges('last_name', this.lastName);
    },
    async savePasswordChange() {
      // Implement password update logic here
      await this.saveFieldChanges('password', this.newPassword);
    },
    async saveFieldChanges(field, value) {
      const token = localStorage.getItem("token");
      if (token && this.isEditable) {
        const updatedData = {
          [field]: value
        };

        try {
          const response = await axiosInstance.patch('/users', updatedData);
          
          if (response.status === 200) {
            // Update local storage with new token
            localStorage.setItem("token", response.data.access_token);

            this.successMessage = true;
            setTimeout(() => {
              this.successMessage = false;
            }, 5000);
          }
        } catch (error) {
          console.error(`Error updating ${field}:`, error);
          alert(`An error occurred while updating ${field}.`);
        }
      }
    }
  }
};
</script>

<style scoped>
.account-details {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  position: relative; /* Ensure positioning context */
}

.account-details h1 {
  font-size: 2em;
  
  color: #333;
  top: 20px;
}

.edit-icon {
  width: 20px;
  height: 20px;
  cursor: pointer;
  display: inline-block;
  background-image: url('edit-icon.png');
  background-size: cover;
  position: absolute;
  top: 20px;
  right: 20px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.user-info.disabled .input {
  background-color: #e9e9e9;
  cursor: not-allowed;
}

.info-item {
  width: 100%;
  padding: 10px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-bottom: 1px solid #ddd;
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
  color: #555;
  margin-bottom: 5px;
}

.input {
  width: 80%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.btn-save {
  padding: 10px 20px;
  border: none;
  background-color: #4caf50;
  color: #fff;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease;
  margin-top: 15px;
}

.btn-save:hover {
  background-color: #45a049;
}

.btn-save:disabled {
  background-color: #9e9e9e;
  cursor: not-allowed;
}

.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #4caf50;
  color: white;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  transition: transform 0.3s ease-out;
}

.notification.success {
  background-color: #4caf50;
}

.notification.error {
  background-color: #f44336;
}

.modal {
  display: block; /* Hidden by default */
  position: fixed;
  z-index: 1000; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
  padding-top: 60px;
}

.modal-content {
  background-color: #fefefe;
  margin: 5% auto; /* 15% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.error-msg {
  color: #f44336;
  font-weight: bold;
  margin-top: 10px;
}
</style>
