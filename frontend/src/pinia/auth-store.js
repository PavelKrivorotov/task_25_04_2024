import { ref} from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth-store', () => {
    const token = ref(null)
    const isAdmin = ref(false)
    const isAuthenticated = ref(false)

    function initStorage() {
        const storageToken = localStorage.getItem('authorization-token')
        token.value = storageToken

        const storageAdmin = localStorage.getItem('is-admin')
        if (storageAdmin == 'true') { isAdmin.value = true }
        else { isAdmin.value = false }

        const storageAuthenticated = localStorage.getItem('is-authenticated')
        if (storageAuthenticated == 'true') { isAuthenticated.value = true }
        else { isAuthenticated.value = false }
    }

    function setToken(newToken) {
        localStorage.setItem('authorization-token', newToken)
        token.value = newToken
    }

    function setAdmin(state) {
        localStorage.setItem('is-admin', state)
        isAdmin.value = state
    }

    function setAuthenticated(state) {
        localStorage.setItem('is-authenticated', state)
        isAuthenticated.value = state
    }

    function clear() {
        localStorage.removeItem('authorization-token')
        token.value = null

        localStorage.removeItem('is-admin')
        isAdmin.value = false

        localStorage.removeItem('is-authenticated')
        isAuthenticated.value = false
    }

    return {
        token,
        isAdmin,
        isAuthenticated,

        initStorage,
        setToken,
        setAdmin,
        setAuthenticated,
        clear
    }
})
