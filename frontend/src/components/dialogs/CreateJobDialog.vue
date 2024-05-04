<script setup>
import { useAuthStore } from '@/pinia/auth-store';
import { adminCreateJob } from '@/http/requests';

import CreateJobForm from '@/components/forms/CreateJobForm.vue'

const authStore = useAuthStore()

const props = defineProps({isActive: Boolean})
const emits = defineEmits([
    'cancel',
    'complete'
])

async function createJob(data) {
    console.log(data)

    try {
        const response = await adminCreateJob(data, authStore.token)
        if (response.status == 201) { emits('complete') }
        else {
            emits('cancel')
            alert('Any servrr error!')
        }

    } catch (error) {
        emits('cancel')
        alert('Internale server error!')
    }
}
</script>

<template>
    <v-dialog
    v-model="props.isActive"
    width="400"
    persistent
    >
        <CreateJobForm
        @cencel="emits('cancel')"
        @submit="createJob"
        ></CreateJobForm>
    </v-dialog>
</template>

<style scoped>
</style>
