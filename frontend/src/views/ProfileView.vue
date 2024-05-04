<script setup>
import { reactive, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

import { useAuthStore } from '@/pinia/auth-store';
import { loadEmployeeMe, loadJobMe } from '@/http/requests';

const router = useRouter()
const route = useRoute()

const authStore = useAuthStore()

const profile = reactive({
    user: {
        id: null,
        username: null,
        firstName: null,
        lastName: null,
        dateOfEmployment: null,
        isAdmin: null,
        isStaff: null
    },
    job: {
        id: null,
        title: null,
        salary: null,
        daysToPromotion: null
    }
})

watch(
    () => route.fullPath,
    async () => {
        try {
            const response1 = await loadEmployeeMe(authStore.token)
            if (response1.status == 200) {
                const data = await response1.json()
                profile.user.id = data['user']['id']
                profile.user.username = data['user']['username']
                profile.user.firstName = data['user']['first_name']
                profile.user.lastName = data['user']['last_name']
                profile.user.dateOfEmployment = data['user']['date_of_employment']
                profile.user.isAdmin = data['user']['is_superuser']
                profile.user.isStaff = data['user']['is_staff']

            } else if (response1.status == 401 || response1.status == 403) {
                router.push({name: 'login'})

            } else {
                alert('Idk in watch (Profile.vue)')   
            }

            const response2 = await loadJobMe(authStore.token)
            if (response2.status == 200) {
                const data = await response2.json()
                profile.job.id = data['job']['id']
                profile.job.title = data['job']['title']
                profile.job.salary = data['job']['salary']
                profile.job.daysToPromotion = data['job']['days_to_promotion']

            } else if (response2.status == 401 || response2.status == 403) {
                router.push({name: 'login'})

            } else {
                alert('Idk in watch (Profile.vue)')   
            }

        } catch (error) {
            alert('Internal server eror')
        }
    },
    {immediate: true}
)
</script>

<template>
    <v-row no-gutters>
        <v-col class="d-flex justify-center">
            <v-card
            width="450"
            >
                <template v-slot:title>
                    Account
                </template>

                <template v-slot:text>
                    <v-form>
                        <v-text-field
                        label="Account UUID"
                        density="comfortable"
                        v-model="profile.user.id"
                        readonly
                        ></v-text-field>

                        <v-text-field
                        label="Username"
                        density="comfortable"
                        v-model="profile.user.username"
                        readonly
                        ></v-text-field>

                        <v-text-field
                        label="Name"
                        density="comfortable"
                        v-model="profile.user.firstName"
                        readonly
                        ></v-text-field>

                        <v-text-field
                        label="Surname"
                        density="comfortable"
                        v-model="profile.user.lastName"
                        readonly
                        ></v-text-field>

                        <v-text-field
                        label="Date of employment"
                        density="comfortable"
                        v-model="profile.user.dateOfEmployment"
                        readonly
                        ></v-text-field>

                        <v-text-field
                        label="Is admin"
                        density="comfortable"
                        v-model="profile.user.isAdmin"
                        ></v-text-field>

                        <v-text-field
                        label="Is staff"
                        density="comfortable"
                        v-model="profile.user.isStaff"
                        readonly
                        ></v-text-field>
                    </v-form>
                </template>
            </v-card>
        </v-col>

        <v-col class="d-flex justify-center">
            <v-card
            width="450"
            >
                <template v-slot:title>
                    Job
                </template>

                <template v-slot:text>
                    <v-text-field
                        label="Job UUID"
                        density="comfortable"
                        v-model="profile.job.id"
                        readonly
                        ></v-text-field>

                        <v-text-field
                        label="Title"
                        density="comfortable"
                        v-model="profile.job.title"
                        readonly
                        ></v-text-field>

                        <v-text-field
                        label="Salary"
                        density="comfortable"
                        v-model="profile.job.salary"
                        readonly
                        ></v-text-field>

                        <v-text-field
                        label="Days to promotion"
                        density="comfortable"
                        v-model="profile.job.daysToPromotion"
                        readonly
                        ></v-text-field>
                </template>
            </v-card>
        </v-col>
    </v-row>
</template>

<style scoped>
</style>
