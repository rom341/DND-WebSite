import { apiRequest } from './base.js';

export const AccountAPI = {
    loginUser: (username, password) => apiRequest('/api/accounts/login', 'POST', {
        "username": username,
        "password": password
    })
};