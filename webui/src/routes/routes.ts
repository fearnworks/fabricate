import * as VueRouter from 'vue-router'
import image from '@/routes/image.vue'

export const Home = { template: '<div>Home</div>' }
export const About = { template: '<div>About</div>' }
const routes = [
    { path: '/', component: Home },
    { path: '/about', component: About },
    { path: '/images/:id', component: image }
]

export const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes
})