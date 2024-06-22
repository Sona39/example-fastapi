// src/main.js
import { createApp } from 'vue';
import AppComponent from './AppComponent.vue'; // Adjust path if necessary
import router from './router';

// Import FontAwesome
import '@fortawesome/fontawesome-free/css/all.css';

// Create a Vue application instance
const app = createApp(AppComponent);

// Use the router with the app instance
app.use(router);

// Mount the app to the DOM
app.mount('#app');
