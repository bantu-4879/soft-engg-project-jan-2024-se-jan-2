import Vue from 'vue';
import VueRouter from 'vue-router';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import store from '../store';
import * as common from "../assets/common.js";
import StudentHome from '../views/StudentHome.vue';
import StudentCreateTicket from '../views/StudentCreateTicket.vue';
import StudentMyTickets from '../views/StudentMyTickets.vue';
import CommonFAQs from '../views/CommonFAQs.vue';
import SupportHome from '../views/SupportHome.vue';
import SupportMyTickets from '../views/SupportMyTickets.vue';
import AdminHome from '../views/AdminHome.vue';
import AdminCreateFAQ from '../views/AdminCreateFAQ.vue';
import AdminValidateUsers from '../views/AdminValidateUsers.vue';
import AppHomeView from '../views/AppHomeView.vue';
import UserProfile from '../views/UserProfile.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    alias: '/home',
    name: 'AppHomeView',
    component: AppHomeView,
  },
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'RegisterView',
    component: RegisterView,
  },
  {
    path: '/student-home',
    name: 'StudentHome',
    component: StudentHome,
  },
  {
    path: '/student-create-ticket',
    name: 'StudentCreateTicket',
    component: StudentCreateTicket,
  },
  {
    path: '/student-my-tickets',
    name: 'StudentMyTickets',
    component: StudentMyTickets,
  },
  {
    path: '/common-faqs',
    name: 'CommonFAQs',
    component: CommonFAQs,
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: UserProfile,
  },
  {
    path: '/support-home',
    name: 'SupportHome',
    component: SupportHome,
  },
  {
    path: '/support-my-tickets',
    name: 'SupportMyTickets',
    component: SupportMyTickets,
  },
  {
    path: '/admin-home',
    name: 'AdminHome',
    component: AdminHome,
  },
  {
    path: '/admin-validate-users',
    name: 'AdminValidateUsers',
    component: AdminValidateUsers,
  },
  {
    path: '/admin-create-faq',
    name: 'AdminCreateFAQ',
    component: AdminCreateFAQ,
  },
  {
    path: '*',
    redirect: '/',
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/register', '/', '/home'];
  const authRequired = !publicPages.includes(to.path);
  if (!store.getters.get_logged_status) {
    store.commit('initialiseStore');
  }
  const logged_status = store.getters.get_logged_status;

  if (authRequired && !logged_status) {
    alert("Token expired. Please log in again.");
    return next('/login');
  }
  if (authRequired && logged_status) {
    const role = store.state.user.role;

    if (((role === 'student') && (common.STUDENT_ROUTES.includes(to.path)))
      || ((role === 'support') && (common.SUPPORT_ROUTES.includes(to.path)))
      || ((role === 'admin') && (common.ADMIN_ROUTES.includes(to.path)))) {
      return next();
    }
    else {
      alert("You don't have access to this page.");
      return next(`/${role}-home`);
    }
  }
  next();
})

export default router;
