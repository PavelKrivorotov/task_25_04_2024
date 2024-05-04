import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/pinia/auth-store"

import LoginView from "@/views/LoginView.vue"
import RegisterView from "@/views/RegisterView.vue"

import ProfileView from "@/views/ProfileView.vue"
import EmployeesView from "@/views/EmployeesView.vue"
import JobsView from "@/views/JobsView.vue"


export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            redirect: {name: 'profile'}
        },
        {
            path: '/auth',
            redirect: {name: 'login'},
            children: [
                {
                    path: 'login',
                    name: 'login',
                    component: LoginView
                },
                {
                    path: 'register',
                    name: 'register',
                    component: RegisterView
                },
            ]
        },
        {
            path: '/profile',
            name: 'profile',
            component: ProfileView
        },
        {
            path: '/jobs',
            name: 'jobs',
            component: JobsView
        },
        {
            path: '/admin',
            redirect: {name: 'admin-employee-profiles'},
            children: [
                {
                    path: 'employees',
                    name: 'admin-employee-profiles',
                    component: EmployeesView
                },
                {
                    path: 'jobs',
                    name: 'admin-jobs',
                    component: JobsView
                }
            ]
        }
    ]
})

router.beforeEach(async (to, from) => {
    const authStore = useAuthStore()
    authStore.initStorage()

    if (to.name == 'profile' && authStore.isAuthenticated == false) { return {name: 'login'} }
    if (to.name == 'profile' && authStore.isAdmin == true) { return {name: 'admin-employee-profiles'} }

    if (to.name == 'jobs' && authStore.isAuthenticated == false) { return {name: 'login'} }
    if (to.name == 'jobs' && authStore.isAdmin == true) { return {name: 'admin-jobs'} }

    if (to.name == 'admin-employee-profiles' && authStore.isAdmin == false) { return {name: 'profile'} }
    if (to.name == 'admin-jobs' && authStore.isAdmin == false) { return {name: 'jobs'} }  
})
