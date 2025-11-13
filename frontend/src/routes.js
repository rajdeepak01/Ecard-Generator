import { createRouter, createWebHashHistory } from "vue-router";
import Content from "./components/Content.vue";
import LoginPage from "./components/LoginPage.vue";
import RegisterPage from "./components/RegisterPage.vue";
import Dashboard from "./components/Dashboard.vue";
import RequestCard from "./components/RequestCard.vue";


const routes = [
    {path: "/", component: Content},
    {path: "/login", component: LoginPage},
    {path: "/register", component: RegisterPage},
    {path: "/dashboard", component: Dashboard},
    {path: "/user/request/:cardname", component: RequestCard}
    // {path: "/user", components:[
    //     {path: "request/:cardname", component: RequestCard},
    //     {path: "view/:cardname", component: ViewCard}
    // ],
    // component: User},

]

export const router = createRouter({
    history: createWebHashHistory(),
    routes
})


