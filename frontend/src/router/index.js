import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "@/stores";
import {
  Home,
  Login,
  IndexEvents,
  ViewEvent,
  IndexUsers,
  IndexOrganisations,
  ViewOrganisation,
  AddUser,
  ViewUsers,
  IndexServers,
  ViewServer,
  EditEvent,
  AddEvent,
} from "@/views";

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: "active",
  routes: [
    { path: "/", component: Home },
    { path: "/login", component: Login },
    { path: "/events", component: IndexEvents },
    { path: "/events/:id", component: ViewEvent, props: true },
    { path: "/events/update/:id", component: EditEvent, props: true },
    { path: "/events/add", component: AddEvent, props: true },
    { path: "/users", component: IndexUsers },
    { path: "/users/add", component: AddUser },
    { path: "/users/:id", component: ViewUsers, props: true },
    { path: "/organisations", component: IndexOrganisations },
    { path: "/organisations/:id", component: ViewOrganisation, props: true },
    { path: "/servers", component: IndexServers },
    { path: "/servers/:id", component: ViewServer, props: true },
  ],
});

router.beforeEach(async (to) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ["/login"];
  const authRequired = !publicPages.includes(to.path);
  const auth = useAuthStore();

  if (authRequired && !auth.isAuthenticated()) {
    auth.returnUrl = to.fullPath;
    return "/login";
  }
});
