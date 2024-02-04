import axios from 'axios';

const Host = "https://chinhtran18.pythonanywhere.com"

export const endpoints = {
    'login': '/login/',
    'current-user': '/user/current-user/',
    'register': '/users/'
}

export const authApi = (accessToken) => axios.create({
    baseURL: Host,
    headers: {
        "Authorization": `Bearer ${accessToken}`
    }
})

export default axios.create({
    baseURL: Host
})