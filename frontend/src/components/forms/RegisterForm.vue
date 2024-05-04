<script setup>
import { ref, reactive, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useForm, useField } from 'vee-validate';
import * as yup from 'yup';

import { useAuthStore } from '@/pinia/auth-store';
import { loadJobs, register, login } from '@/http/requests';

const route = useRoute()
const router = useRouter()

const authStore = useAuthStore()

const loadingJobs = ref(true)
const jobItems = reactive([])

const { handleSubmit, setFieldError } = useForm({
    validationSchema: yup.object({
        username: yup.string().max(128).required(),
        password: yup.string().max(128).required(),
        firstName: yup.string().max(150).required(),
        lastName: yup.string().max(150).required(),
        job: yup.string().required()
    })
})

const username = useField('username')
const password = useField('password')
const firstName = useField('firstName')
const lastName = useField('lastName')
const job = useField('job')

const submit = handleSubmit(async (values) => {
    const data1 = new FormData()
    data1.append('username', values.username)
    data1.append('password', values.password)
    data1.append('first_name', values.firstName)
    data1.append('last_name', values.lastName)
    data1.append('job_id', values.job)

    try {
        const response1 = await register(data1)
        if (response1.status == 201) {
            const data2 = new FormData()
            data2.append('username', values.username)
            data2.append('password', values.password)

            try {
                const response2 = await login(data2)
                if (response2.status == 200) {
                    const data = await response2.json()
                    authStore.setToken(data['access_token'])
                    authStore.setAdmin(data['is_superuser'])
                    authStore.setAuthenticated(true)

                    if (authStore.isAdmin) { router.push({name: 'admin-employee-profiles'}) }
                    else { router.push({name: 'profile'}) }

                } else if (response2.status == 400) {
                    setFieldError('username', 'Invalid username or password')
                    setFieldError('password', 'Invalid username or password')

                } else { alert('Internal server error!') }

            } catch (error) { alert('Servr error on login after register!') }

        } else if (response1.status == 400) {
            setFieldError('username', 'username already exists')

        } else { alert('Any error!') }

    } catch (error) { alert('Internal server error!') }
})

watch(
    () => route.fullPath,
    async () => {
        try {
            const response = await loadJobs()
            if (response.status == 200) {
                const data = await response.json()
                data['results'].forEach(item => {jobItems.push(item)});
                loadingJobs.value = false
            }

        } catch (error) { alert('Internal server error!') }
    },
    {immediate:true}
)
</script>

<template>
    <v-card
    width="450px"
    rounded="8"
    elevation="3"
    >
        <template v-slot:text>
            <v-form>
                <v-text-field
                label="Username"
                density="comfortable"
                v-model="username.value.value"
                :error-messages="username.errorMessage.value"
                ></v-text-field>

                <v-text-field
                label="Password"
                density="comfortable"
                type="password"
                v-model="password.value.value"
                :error-messages="password.errorMessage.value"
                class="pt-2"
                ></v-text-field>

                <v-text-field
                label="Name"
                density="comfortable"
                v-model="firstName.value.value"
                :error-messages="firstName.errorMessage.value"
                class="pt-2"
                ></v-text-field>

                <v-text-field
                label="Surname"
                density="comfortable"
                v-model="lastName.value.value"
                :error-messages="lastName.errorMessage.value"
                class="pt-2"
                ></v-text-field>

                <v-select
                label="Job"
                density="comfortable"
                item-title="title"
                item-value="id"
                v-model="job.value.value"
                :error-messages="job.errorMessage.value"
                :items="jobItems"
                :loading="loadingJobs"
                class="pt-2"
                ></v-select>
            </v-form>
        </template>

        <template v-slot:actions>
            <v-spacer></v-spacer>
            <v-btn @click="submit">Submit</v-btn>
        </template>
    </v-card>
</template>

<style scoped>
</style>
