<script setup>
import { reactive, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/pinia/auth-store';
import { adminLoadEmployees } from '@/http/requests';

const route = useRoute()
const router = useRouter()

const authStore = useAuthStore()

const employeeHeaders = reactive([
    {title: 'User ID', key: 'userId'},
    {title: 'Username', key: 'username'},
    {title: 'Name', key: 'firstName'},
    {title: 'Surname',key: 'lastName'},
    {title: 'Date of employment', key: 'dateOfEmployment'},
    {title: 'Is admin', key: 'isAdmin'},
    {title: 'Is staff', key: 'isStaff'},
    {title: 'Title', key: 'title'},
    {title: 'Salary', key: 'salary'},
    {title: 'Days to promotion', key: 'daysToPromotion'}
])

const employeeItems = reactive([])

watch(
    () => route.fullPath,
    async () => {
        try {
            const response = await adminLoadEmployees(authStore.token)
            if (response.status == 200) {
                const data = await response.json()
                setEmployeeItems(data['results'])

            } else if (response.status == 401 || response.status == 403) {
                router.push({name: 'profile'})

            } else { alert('Internal server error!') }

        } catch (error) { alert('Internal servrr error') }
    },
    {immediate: true}
)

function setEmployeeItems(data) {
    data.forEach(item => {
        employeeItems.push({
            userId: item['user']['id'],
            username : item['user']['username'],
            firstName: item['user']['first_name'],
            lastName: item['user']['last_name'],
            dateOfEmployment: item['user']['date_of_employment'],
            isAdmin: item['user']['is_superuser'],
            isStaff: item['user']['is_staff'],

            title: item['job']['title'],
            salary: item['job']['salary'],
            daysToPromotion: item['job']['days_to_promotion'],
        })
    })
}
</script>

<template>
    <v-row class="h-100 overflow-width">
        <v-col>
            <v-data-table-virtual
            :headers="employeeHeaders"
            :items="employeeItems"
            item-value="userId"
            ></v-data-table-virtual>
        </v-col>
    </v-row>
</template>

<style scoped>
    .overflow-width{
        overflow-x: scroll;
    }
</style>
