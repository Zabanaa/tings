import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import Home from './Home.vue'
import List from './List.vue'

Vue.use(VueRouter)

const routes = [

    { path: "/", component: Home },
    { path: "/list", component: List }

]

const router = new VueRouter({ routes })

new Vue({
    router,
    el: "#app3",
    render: h => h(App)
})
