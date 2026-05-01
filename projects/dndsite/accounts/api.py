from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, auth
from rest_framework.response import Response
from rest_framework import status
from accounts.schemas import UserDescriptionSchema, UserRegisterSchema, UserLoginSchema
from service.account_services import authenticate_user, logout_user, register_new_user


app = NinjaAPI()

@app.get("accounts/description/{account_id}", response=UserDescriptionSchema)
def get_account_description(request, account_id: int):
    return get_object_or_404(User, id=account_id)

@app.post("accounts/register", response=UserDescriptionSchema)
def register_user(request, user: UserRegisterSchema):
    try:
        user_data = user.model_dump()
        new_user = register_new_user(**user_data)
        authenticated_user = authenticate_user(**user_data)

        auth.login(request, authenticated_user)
        return authenticated_user
    except:
        Response(status=status.HTTP_403_FORBIDDEN)

@app.post("accounts/login", response=UserDescriptionSchema)
def login_user(request, user: UserLoginSchema):
    try:
        user_data = user.model_dump()
        authenticated_user = authenticate_user(**user_data)

        auth.login(request, authenticated_user)
        return authenticated_user
    except:
        Response(status=status.HTTP_403_FORBIDDEN)

@app.post("accounts/logout")
def logout(request):
    logout_user(request=request)