from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpRequest 

def authenticate_user(username: str, password: str, *args, **kwargs) -> User:
    user = auth.authenticate(username=username, password=password)
    if not user:
        raise ValueError("Wrong credentials")
    return user

def register_new_user(username:str, password:str, email:str, first_name:str, last_name:str, *args, **kwargs) -> User:
    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    return user

def logout_user(request: HttpRequest):
    auth.logout(request=request)
