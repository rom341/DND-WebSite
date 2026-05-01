import { apiRequest } from './base.js';

export const AccountAPI = {
    loginUser: (username, password) => apiRequest('/api/accounts/login', 'POST', {
        "username": username,
        "password": password
    }),
    registerUser: (username, email, password, firstname, lastname) => apiRequest('/api/accounts/register', 'POST', {
        "username": username,
        "email": email,
        "password": password,
        "first_name": firstname,
        "last_name": lastname
    }),
    logoutUser: () => apiRequest('/api/accounts/logout', 'POST')
};