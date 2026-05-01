import { AccountAPI } from '../../../core/js/api/account.js';

async function sendRegisterUserMessage() {
    const mainContainer = document.getElementById("register-user-widget-content");

    const usernameElement = mainContainer.querySelector('#id_username');
    const emailElement = mainContainer.querySelector('#id_email');
    const password1Element = mainContainer.querySelector("#id_password1");
    const password2Element = mainContainer.querySelector("#id_password2");
    const firstnameElement = mainContainer.querySelector('#id_first_name');
    const lastnameElement = mainContainer.querySelector('#id_last_name');
    if (password1Element.value !== password2Element.value) {
        return;
    }

    const response = await AccountAPI.registerUser(
        usernameElement.value, 
        emailElement.value, 
        password1Element.value,
        firstnameElement.value,
        lastnameElement.value
    );

    if (response.status == 200) {
        // go to previous page
        const nextUrl = document.referrer || '/';
        window.location.href = nextUrl;    
    }
    else {
        window.alert("Wrong credentials");
    }
}

async function initRegisterUserWidget() {
    document.getElementById('register-user-widget-button').addEventListener('click', async (e) => {
        await sendRegisterUserMessage();
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    await initRegisterUserWidget();
});