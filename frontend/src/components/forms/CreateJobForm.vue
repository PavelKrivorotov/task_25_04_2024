<script setup>
import { useForm, useField } from 'vee-validate';
import * as yup from 'yup';

const emits = defineEmits([
    'cencel',
    'submit'
])

const { handleSubmit } = useForm({
    validationSchema: yup.object({
        title: yup.string().max(150).required(),
        salary: yup.number().min(0).max(1000000).required(),
        daysToPromotion: yup.number().integer().required()
    })
})

const title = useField('title')
const salary = useField('salary')
const daysToPromotion = useField('daysToPromotion')

const submit = handleSubmit(async (values) => {
    const data = new FormData()
    data.append('title', values.title)
    data.append('salary', values.salary)
    data.append('days_to_promotion', values.daysToPromotion)

    emits('submit', data)
})
</script>

<template>
    <v-card
    rounded="8"
    elevation="3"
    >
        <template v-slot:text>
            <v-form
            @submit.prevent="submit"
            >
                <v-text-field
                label="Title"
                density="comfortable"
                v-model="title.value.value"
                :error-messages="title.errorMessage.value"
                ></v-text-field>

                <v-text-field
                label="Salary"
                density="comfortable"
                v-model="salary.value.value"
                :error-messages="salary.errorMessage.value"
                class="pt-2"
                ></v-text-field>

                <v-text-field
                label="Days to promotion"
                density="comfortable"
                v-model="daysToPromotion.value.value"
                :error-messages="daysToPromotion.errorMessage.value"
                class="pt-2"
                ></v-text-field>

                <div class="d-flex justify-end pt-2">
                    <v-btn type="button" @click="emits('cencel')">Cencel</v-btn>
                    <v-btn type="submit" class="ml-2">Create</v-btn>
                </div>
            </v-form>
        </template>
    </v-card>
</template>

<style scoped>
</style>
