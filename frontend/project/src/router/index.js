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
        path: '/hyps/online',
        name: 'HYPS',

        component: () =>
            import ('../views/HYPS-canvas/online.vue')
    },
    {
        path: '/hyps-dom/online',
        name: 'HYPS-Dom',

        component: () =>
            import ('../views/HYPS/online.vue')
    }
]

const router = new VueRouter({
    routes
})

export default router