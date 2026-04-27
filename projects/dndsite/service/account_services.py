from django.contrib.auth.models import User, auth 

def authenticate_user(username: str, password: str) -> User:
    user = auth.authenticate(username=username, password=password)
    if not user:
        raise ValueError("Wrong credentials")
    return user
