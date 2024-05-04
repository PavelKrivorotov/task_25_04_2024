<script setup>
import { useRouter } from 'vue-router';
import { useField, useForm } from 'vee-validate';
import * as yup from 'yup'

import { login } from '@/http/requests';
import { useAuthStore } from '@/pinia/auth-store';

const router = useRouter()
const authStore = useAuthStore()

const { handleSubmit, setFieldError } = useForm({
    validationSchema: yup.object({
        username: yup.string().max(128).required(),
        password: yup.string().max(128).required()
    })
})

const username = useField('username')
const password = useField('password')

const submit = handleSubmit(async (values) => {
    const data = new FormData()
    data.append('username', values.username)
    data.append('password', values.password)

    try{
        const response = await login(data)
        if (response.status == 200) {
            const data = await response.json()
            authStore.setToken(data['access_token'])
            authStore.setAdmin(data['is_superuser'])
            authStore.setAuthenticated(true)

            if (authStore.isAdmin) { router.push({name: 'admin-employee-profiles'}) }
            else { router.push({name: 'profile'}) }

        } else if (response.status == 400) {
            setFieldError('username', 'Invalid username or password')
            setFieldError('password', 'Invalid username or password')

        } else {
            alert('Internal server error!')
        }

    } catch (error) {
        console.error(error)
        alert('Internal server error!')
    }
})
</script>

<template>
    <v-card
    width="400px"
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
