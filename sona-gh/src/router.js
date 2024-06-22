import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue'; // Adjust path if necessary
import LoginView from './views/LoginView.vue'; // Adjust path if necessary
import RegisterView from './views/RegisterView.vue'; // Adjust path if necessary
import PostFeed from './components/PostFeed.vue';
import PostDetailsComponent from './components/PostDetailsComponent.vue';
import CreatePostComponent from './components/CreatePostComponent.vue';
import UpdatePostComponent from './components/UpdatePostComponent.vue';
import ProtectedResource from './components/ProtectedResource.vue'; // Adjust path if necessary
import AccountDetailsComponent from './components/AccountDetailsComponent.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/post-feed', name: 'PostFeed', component: PostFeed },
  { path: '/posts/:id', name: 'PostDetails', component: PostDetailsComponent, props: true },
  { path: '/create', name: 'CreatePost', component: CreatePostComponent },
  { path: '/update/:id', name: 'UpdatePost', component: UpdatePostComponent, props: true },
  { path: '/protected-resource', name: 'ProtectedResource', component: ProtectedResource },
  {path: '/account', name: 'AccountDetails', component: AccountDetailsComponent}
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
  

