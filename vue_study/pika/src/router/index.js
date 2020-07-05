import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/Home.vue'
import Forum from '@/views/Forum'
import Write from '@/components/WritePage'


Vue.use(Router)

const routes = [{
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/about',
        name: 'About',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import ( /* webpackChunkName: "about" */ '../views/About.vue')
    }, {
        path: '/forum',
        name: 'Forum',
        component: Forum
    }, {
        path: '/write',
        name: 'Write',
        component: Write
    }, {
        path: '*',
        redirect: "/"
    }
]

const router = new Router({
    mode: 'history',
    routes
})

export default router