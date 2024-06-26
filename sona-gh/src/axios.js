import axios from 'axios';
const apiHost = process.env.VUE_APP_API_HOST;


const axiosInstance = axios.create({
  baseURL: apiHost, // Update with your API base URL
  headers: {
    'Content-Type': 'application/json'
  }
});

axiosInstance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login'; // Adjust the route to your login page
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;