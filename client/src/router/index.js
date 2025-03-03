import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/pages/Home.vue';
import UserPage from '@/pages/UserPage.vue';

const fetchUsersFromAPI = async () => {
  try {
    const response = await fetch('http://localhost:5001/users');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching users:', error);
    return [];
  }
};

const fetchUserFromAPI = async (id) => {
  try {
    const response = await fetch(`http://localhost:5001/users/${id}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching user:', error);
    return null;
  }
};

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    props: true, 
    beforeEnter: async (to, from, next) => {
      const users = await fetchUsersFromAPI();
      to.params.users = users; 
      next();
    },
  },
  {
    path: '/user/:id',
    name: 'UserPage',
    component: UserPage,
    props: true, 
    beforeEnter: async (to, from, next) => {
      const userId = to.params.id;
      const user = await fetchUserFromAPI(userId);
      if (user) {
        to.params.user = user; 
        next();
      } else {
        next({ name: 'Home' }); 
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
