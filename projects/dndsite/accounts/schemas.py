from ninja import ModelSchema, Schema

from django.contrib.auth.models import User

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"


class UserRegisterSchema(Schema):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    

class UserLoginSchema(Schema):
    username: str
    password: str

class UserDescriptionSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["username", "email"]
        
