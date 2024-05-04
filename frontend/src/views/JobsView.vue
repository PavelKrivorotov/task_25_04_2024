<script setup>
import { reactive, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/pinia/auth-store';
import { loadJobs, adminLoadJobs } from '@/http/requests';

import CreateJobDialog from '@/components/dialogs/CreateJobDialog.vue';

const route = useRoute()
const router = useRouter()

const authStore = useAuthStore()

const isActiveCreateDialog = ref(false)

const jobHeaders = reactive([
    {title: 'UUID', key: 'id'},
    {title: 'Title', key: 'title'}
])

const adminJobHeaders = reactive([
    {title: 'UUID', key: 'id'},
    {title: 'Title', key: 'title'},
    {title: 'Salary', key: 'salary'},
    {title: 'Days to promotion', key: 'daysToPromotion'}
])

const jobItems = reactive([])

watch(
    () => route.fullPath,
    async () => {
        if (authStore.isAdmin) {
            try {
                const response = await adminLoadJobs(authStore.token)
                if (response.status == 200) {
                    const data = await response.json()
                    setJobItems(data['results'])

                } else if (response.status == 401 || response.status == 403) {
                    router.push({name: 'jobs'})

                } else { alert('Internal server errror!') }

            } catch (error) { alert('Inernal server error!') }

        } else {
            try{
                const response = await loadJobs()
                if (response.status == 200) {
                    const data = await response.json()
                    setJobItems(data['results'])
                }

            } catch (error) {
                alert('Internal server error')
            }
        }
    },
    {immediate: true}
)

async function refreshJobs() {
    isActiveCreateDialog.value = false

    try {
        const response = await adminLoadJobs(authStore.token)
        if (response.status == 200) {
            const data = await response.json()
            jobItems.splice(0, jobItems.length)
            setJobItems(data['results'])

        } else { alert('Internal server errror!') }

    } catch (error) { alert('Inernal server error!') }
}

function setJobItems(data) {
    data.forEach(item => {
        jobItems.push({
            id: item['id'],
            title: item['title'],
            salary: item['salary'],
            daysToPromotion: item['days_to_promotion']
        })
    })
}
</script>

<template>
    <v-row class="h-100 overflow-width">
        <v-col>
            <template v-if="authStore.isAdmin">
                <div class="d-flex justify-end pb-3">
                    <v-btn @click="isActiveCreateDialog = true">Create job</v-btn>
                </div>

                <v-data-table-virtual
                :headers="adminJobHeaders"
                :items="jobItems"
                item-value="id"
                ></v-data-table-virtual>

                <div>
                    <CreateJobDialog
                    :is-active="isActiveCreateDialog"
                    @cancel="isActiveCreateDialog = false"
                    @complete="refreshJobs"
                    ></CreateJobDialog>
                </div>
            </template>

            <template v-else>
                <v-data-table-virtual
                :headers="jobHeaders"
                :items="jobItems"
                item-value="id"
                ></v-data-table-virtual>
            </template>
        </v-col>
    </v-row>
</template>

<style scoped>
.overflow-width{
    overflow-x: scroll;
}
</style>
