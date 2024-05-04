<script setup>
import { useRouter, RouterView } from 'vue-router';

import { useAuthStore } from './pinia/auth-store';
import { logout } from './http/requests';

const router = useRouter()
const authStore = useAuthStore()

async function btnLogout() {
    try{
        const response = await logout(authStore.token)
        if (response.status == 200 || response.status == 401) {
            authStore.clear()
            router.push({name: 'login'})
        }

    } catch (error) {
        alert('Internal server error!')
    }
}
</script>

<template>
    <v-layout>
        <template v-if="authStore.isAuthenticated">
            <v-app-bar
            elevation="1"
            >
                <template v-if="authStore.isAdmin" v-slot:prepend>
                    <v-btn to="/admin/employees">Employees</v-btn>
                    <v-btn to="/admin/jobs">Jobs (Vacancies)</v-btn>
                </template>

                <template v-else v-slot:prepend>
                    <v-btn to="/profile">Profile</v-btn>
                    <v-btn to="/jobs">Jobs (Vacancies)</v-btn>
                </template>

                <template v-slot:append>
                    <v-btn @click="btnLogout">Logout</v-btn>
                </template>
            </v-app-bar>
        </template>

        <template v-else>
            <v-app-bar
            elevation="1"
            >
                <template v-slot:append>
                    <v-btn to="/auth/login">Sign in</v-btn>
                    <v-btn to="/auth/register">Sign up</v-btn>
                </template>
            </v-app-bar>
        </template>

        <v-main class="full-height">
            <v-container class="fill-height">
                <RouterView/>
            </v-container>
        </v-main>
    </v-layout>
</template>

<style scoped>
.full-height{
    height: 100dvh;
}
</style>
