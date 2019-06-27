from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, UserManager, Login, LoginManager
import bcrypt


def index(request):

    context = {
        "string" : "Test string for LOGIN PAGE working!",
    }

    return render(request, "login_app/index.html", context)


def register_user(request):
    errors = User.objects.reg_validator(request.POST)

    if len(errors) > 0:
        print("*_*_*_*_*_*_*_*_")
        print("ERRORS IN REGISTRATION")
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        new_user_firstName = request.POST["fname"]
        new_user_lastName = request.POST["lname"]
        new_user_email = request.POST["email"]
        new_user_password = request.POST["password"]

        pw_hash = bcrypt.hashpw(new_user_password.encode(), bcrypt.gensalt())
        print(pw_hash)

        new_user = User.objects.create(
            first_name=new_user_firstName,
            last_name=new_user_lastName,
            email_address=new_user_email,
            password=pw_hash,
            logged_in=True,
        )    
        Login.objects.create(user= new_user)
        request.session['user_id'] = new_user.id

        return redirect("/timeline")

def login_user(request):
    errors = Login.objects.login_validator(request.POST)

    login_email = request.POST["email"]
    login_password = request.POST["password"]

    all_logins = Login.objects.all()

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect("/")
    else:
        for login in all_logins:
            if login_email == login.user.email_address and bcrypt.checkpw(login_password.encode(),login.user.password.encode()):
                user_id = login.user.id
                user = User.objects.get(id=user_id)
                user.logged_in = True
                user.save()
                request.session['user_id'] = user.id
                print(f"***** MATCHED DATA | LOGGED {user.first_name} {user.last_name} STATUS AS: {user.logged_in}")
                return redirect("/timeline")

def logout_user(request):
    try:
        user_id = request.session['user_id']
    except:
        return redirect("/")

    user = User.objects.get(id=user_id)

    user.logged_in = False
    user.save()

    request.session.clear()

    return redirect("/")


def session_test(request):
    try:
        user_id = request.session['user_id']
    except:
        return redirect("/")

    user = User.objects.get(id=user_id)

    context = {
        "user" : user,
        "user_id" : user_id
    }

    return render(request, "login_app/session-test.html", context)

