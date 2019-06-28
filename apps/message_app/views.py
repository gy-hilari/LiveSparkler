from django.shortcuts import render, HttpResponse, redirect

from .models import Message, Firework, FireworkInventory, DeployedFirework

from ..login_app.models import User
from django.contrib import messages

from random import randint, randrange


def index(request):
    try:
        user_id = request.session['user_id']
    except:
        return redirect("/")

    user = User.objects.get(id=user_id)
    all_messages = Message.objects.all().order_by("-created_at")

    context = {
        "string" : "test string for message app working!",
        "user" : user,
        "user_id" : user_id,
        "all_messages" : all_messages,
    }

    return render(request, "message_app/message-index.html", context)

def new_message(request):
    try:
        user_id = request.session['user_id']
    except:
        return redirect("/")

    errors = Message.objects.message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect("/timeline") 
    else:
        user = User.objects.get(id=user_id)

        created_message = Message.objects.create(
            user= user,
            message= request.POST["message-text"]
        )

        return redirect("/timeline")

def delete_message(request, message_id):
    if request.method == "GET":
        return redirect("/timeline")
    if request.method == "POST":
        try:
            user_id = request.session['user_id']
        except:
            return redirect("/")

        user = User.objects.get(id=user_id)
        message = Message.objects.get(id=message_id) 

        message.delete()

        return redirect("/timeline")

def view_message(request, message_id):
    try:
        user_id = request.session['user_id']
    except:
        return redirect("/")

    user = User.objects.get(id=user_id)
    target_message = Message.objects.get(id=message_id) 

    all_user_fireworks = FireworkInventory.objects.filter(user=user).order_by("-created_at")
    user_firework_log = {}
    for i in range(len(all_user_fireworks)):
        try:
            user_firework_log[all_user_fireworks[i].firework.name] += 1
        except:
            user_firework_log[all_user_fireworks[i].firework.name] = 1

    recieved_fireworks = DeployedFirework.objects.filter(message=target_message).order_by("-created_at")
    message_firework_log = {}
    for i in range(len(recieved_fireworks)):
        try:
            message_firework_log[recieved_fireworks[i].firework.name] += 1
        except:
            message_firework_log[recieved_fireworks[i].firework.name] = 1

    total_recieved_fireworks = recieved_fireworks.count()
    

    context = {
        "user" : user,
        "message" : target_message,
        "user_firework_log" : user_firework_log,
        "message_firework_log" : message_firework_log,
        "total_recieved_fireworks" : total_recieved_fireworks,
    }

    return render(request, "message_app/view-message.html", context)

def get_fireworks(request):
    try:
        user_id = request.session['user_id']
    except:
        return redirect("/")


    user = User.objects.get(id=user_id)
    all_fireworks = Firework.objects.all()

    firework_drop_count = randint(1,10)
    random_firework_id = []
    random_fireworks = [] 

    for i in range(0, firework_drop_count, 1):
        random_firework_id.append(all_fireworks[randint(0,len(all_fireworks)-1)].id)
    for i in range(len(random_firework_id)):
        firework = Firework.objects.get(id=random_firework_id[i])

        print("%*%*%*%*%*%*%*%*%*%*%*%*%*%*%")
        print(f"{firework.name} added to User# {user.id}'s inventory'")

        random_fireworks.append(firework.name)

        new_firework_supply = FireworkInventory.objects.create(
            user= user,
            firework= firework
        )

        print(new_firework_supply)

    # for i in range(len(all_fireworks)):
    #     random_fireworks.append(all_fireworks[i].name)

    # ANALYZE USER LEVEL || if user.user_level < 3 etc...

    context = {
        "user" : user,
        "all_fireworks" : all_fireworks,
        "random_fireworks" : random_fireworks,
    }

    return render(request, "message_app/get-fireworks.html", context)

def view_user_fireworks(request):
    try:
        user_id = request.session['user_id']
    except:
        return redirect("/")

    user = User.objects.get(id=user_id)
    all_user_fireworks = FireworkInventory.objects.filter(user=user).order_by("-created_at")

    user_firework_log = {}
    for i in range(len(all_user_fireworks)):
        try:
            user_firework_log[all_user_fireworks[i].firework.name] += 1
        except:
            user_firework_log[all_user_fireworks[i].firework.name] = 1

    # user_firework_names = []
    for item in user_firework_log:
        print("%*%*%*%*%*%*%*%*%*%*%*%")
        print(item)
        print("%*%*%*%*%*%*%*%*%*%*%*%")
        # user_firework_names.append(item)

    # for i in range(len(all_user_fireworks)):
        # user_firework_names.append(all_user_fireworks[i].firework.name)

    context = {
        "user" : user,
        "all_user_fireworks" : all_user_fireworks,
        # "user_firework_names" : user_firework_names,
        "user_firework_log" : user_firework_log
    }

    return render(request, "message_app/firework-inventory.html", context)

def deploy_firework(request, message_id, firework_name):
    if request.method == "GET":
        return redirect("/timeline")
    if request.method == "POST":
        try:
            user_id = request.session['user_id']
        except:
            return redirect("/")

        user = User.objects.get(id=user_id)        
        firework = Firework.objects.get(name=firework_name)
        message = Message.objects.get(id=message_id)

        firework_log = FireworkInventory.objects.filter(user=user, firework=firework).first()

        DeployedFirework.objects.create(
            message= message,
            sent_by= user,
            firework= firework
        )

        firework_log.delete()
        
        
        return redirect("/view_message/" + message_id)


