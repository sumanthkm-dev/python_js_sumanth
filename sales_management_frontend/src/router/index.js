import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import DashBoardView from "../views/DashBoardView.vue";
import ErrorPageView from "../views/ErrorPageView.vue";

const routes = [
  {
    path: "/",
    name: "LoginView",
    component: LoginView,
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: DashBoardView,
  },
  {
    path: "/error",
    name: "ErrorPageView",
    component: ErrorPageView,
  },
  {
    // Default route for any invalid endpoint
    path: "/:pathMatch(.*)*",
    redirect: "/",
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
