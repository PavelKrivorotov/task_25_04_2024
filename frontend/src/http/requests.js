import * as urls from '@/http/urls';
import * as settings from '@/settings'


export const baseUrl = settings.HTTP_PROTOCOL + '://' + settings.BACKEND_HOST + ':' + settings.BACKEND_PORT


function make_authorization_header(token) {
    const tok = 'Bearer ' + token
    return tok
}


export async function register(data) {
    const url = baseUrl + urls.AUTH_REGISTER
    const response = await fetch(
        url,
        {
            method: 'POST',
            body: data
        }
    )

    return response
}


export async function login(data) {
    const url = baseUrl + urls.AUTH_LOGIN
    const response = await fetch(
        url,
        {
            method: 'POST',
            body: data
        }
    )

    return response
}


export async function logout(token) {
    const url = baseUrl + urls.AUTH_LOGOUT
    const response = await fetch(
        url,
        {
            method: 'POST',
            headers: {
                'Authorization': make_authorization_header(token)
            }
        }
    )

    return response
}


export async function loadEmployeeMe(token) {
    const url = baseUrl + urls.EMPLOYEE_ME
    const response = await fetch(
        url,
        {
            headers: {
                'Authorization': make_authorization_header(token)
            }
        }
    )

    return response
}


export async function loadJobMe(token) {
    const url = baseUrl + urls.JOB_ME
    const response = await fetch(
        url,
        {
            headers: {
                'Authorization': make_authorization_header(token)
            }
        }
    )

    return response
}

export async function loadJobs() {
    const url = baseUrl + urls.JOBS_ALL
    const response = await fetch(url)
    return response
}


export async function adminCreateJob(data, token) {
    const url = baseUrl + urls.ADMIN_JOB_CREATE
    const response = await fetch(
        url,
        {
            method: 'POST',
            body: data,
            headers: {
                'Authorization': make_authorization_header(token)
            }
        }
    )

    return response
}


export async function adminLoadEmployees(token) {
    const url = baseUrl + urls.ADMIN_EMPLOYEE_ALL
    const response = await fetch(
        url,
        {
            headers: {
                'Authorization': make_authorization_header(token)
            }
        }
    )

    return response
}


export async function adminLoadJobs(token) {
    const url = baseUrl + urls.ADMIN_JOB_ALL
    const response = await fetch(
        url,
        {
            headers: {
                'Authorization': make_authorization_header(token)
            }
        }
    )

    return response
}
