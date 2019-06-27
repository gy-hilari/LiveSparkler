from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):

    def reg_validator(self, postData):
        errors = {}

        email_pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

        password_req_lower = '[a-z]'
        password_req_upper = '[A-Z]'
        password_req_symbol = '[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]'
        

        print(re.findall(password_req_lower, postData["password"]))

        print(postData)

        if User.objects.filter(email_address=postData["email"]).exists():
            errors["email"] = "Account for this email already exists!"

        if postData["confirm-password"] != postData["password"]:
            print("Here!")
            errors["password"] = "Passwords do not match!"

        if len(postData["password"]) < 8:
            print("Also Here!")
            errors["pw-length"] = "Password must be at least 8 characters!"

        if len(postData["password"]) >= 20:
            print("Also Here!")
            errors["pw-length2"] = "Password must be under 20 characters!"
        
        if not re.findall(password_req_lower, postData["password"]):
            errors["no-low"] = "Lowercase character required in password"
        if not re.findall(password_req_upper, postData["password"]):
            errors["no-up"] = "Uppercase character required in password"
        if not re.findall(password_req_symbol, postData["password"]):
            errors["no-sym"] = "Symbol character required in password"

        if len(postData["fname"]) < 3:
            errors["f-name"] = "First name must be at least 3 characters!"

        if len(postData["lname"]) < 3:
            errors["l-name"] = "Last name must be at least 3 characters!"

        if len(postData["fname"]) >= 50:
            errors["f-name"] = "First name cannot exceed 50 characters!"

        if len(postData["lname"]) >= 50:
            errors["l-name"] = "Last name cannot exceed 50 characters!"

        if not re.match(email_pattern, postData["email"], re.I):
            errors["invalid-email"] = "Please enter a valid email address"
                
        return errors 


class User(models.Model):
    first_name = models.CharField(max_length=45, null=True)
    last_name = models.CharField(max_length=45, null=True)
    email_address = models.CharField(max_length=145, null=True)
    password = models.CharField(max_length=45, null=True)
    logged_in = models.BooleanField(default=False)

    user_level = models.IntegerField(default=0)

    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __repr__(self):
        return f"User: {self.first_name} {self.last_name} |  ID: {self.id}"


class LoginManager(models.Manager):
    def login_validator(self, postData):
        errors = {}

        all_logins = Login.objects.all()

        for login in all_logins:
            if postData["email"] == login.user.email_address and bcrypt.checkpw(postData["password"].encode(), login.user.password.encode()):
                return errors

        errors["invalid"] = "Incorrect email or password!"
        return errors


class Login(models.Model):
    user = models.ForeignKey(User, related_name="login", null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = LoginManager()

    def __repr__(self):
        return f"Login Register: {self.user.email_address}   |   {self.user.password}"

