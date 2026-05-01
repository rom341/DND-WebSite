import { AccountAPI } from '../../../core/js/api/account.js';

async function sendLogoutUserMessage() {
    const response = await AccountAPI.logoutUser();
    if (response.status == 200) {
        window.location.href = '/accounts/login/';   
    }
    else {
        window.alert("Can`t logout");
    }
}

async function initLogoutUserWidget() {
    document.getElementById('logout-button').addEventListener('click', async (e) => {
        await sendLogoutUserMessage();
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    await initLogoutUserWidget();
});