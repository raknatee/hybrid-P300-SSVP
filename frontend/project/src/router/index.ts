import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import Home from "../views/Home.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: '/hyps/:mode',
    name: 'HYPS',

    component: () =>
        import ('../views/HYPS/Home.vue')
},
  {
    path: '/dbview',
    name: "DBView",
    component: () =>
        import("../views/DBView/Home.vue")
    
  }
  // {
  //   path: "/about",
  //   name: "About",
   
  //   component: () =>
  //     import("../views/About.vue"),
  // },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
