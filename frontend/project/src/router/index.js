import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [{
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/hyps/:mode',
        name: 'HYPS',

        component: () =>
            import ('../views/HYPS-canvas/Home.vue')
    },
    {
        path: '/dbview',
        name: "DBView",
        component: () =>
            import("../views/DBView/Home.vue")
        
    }

]

const router = new VueRouter({
    routes
})

export default router