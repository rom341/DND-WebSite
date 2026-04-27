import { AccountAPI } from '../../../core/js/api/account.js';

async function sendLoginUserMessage() {
    const mainContainer = document.getElementById("login-user-widget-content");

    const usernameElement = mainContainer.querySelector('#id_username');
    const passwordElement = mainContainer.querySelector("#id_password");
    const response = await AccountAPI.loginUser(usernameElement.value, passwordElement.value);
    console.log(response.status)
    if (response.status == 200) {
        // go to previous page
        const nextUrl = document.referrer || '/';
        window.location.href = nextUrl;    
    }
    else {
        window.alert("Wrong credentials");
    }
}

async function initLoginUserWidget() {
    document.getElementById('login-user-widget-button').addEventListener('click', async (e) => {
        await sendLoginUserMessage();
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    await initLoginUserWidget();
});