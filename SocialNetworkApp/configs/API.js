import axios from "axios"

const HOST = "https://chinhtran18.pythonanywhere.com"

export const endpoints = {
    'login': '/login/',
    'current-user': '/users/current-user/',
    'register': '/users/',
}

export const authApi = (accessToken) => axios.create({
    baseURL: HOST,
    headers: {
        "Authorization": `bearer ${accessToken}`
    }
})

export default axios.create({
    baseURL: HOST
})