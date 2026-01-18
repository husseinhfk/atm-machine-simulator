from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Account

@login_required
def set_pin(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        pin = request.POST.get("pin")

        if pin and pin.isdigit() and len(pin) == 4:
            account.set_pin(pin)
            account.save()
            return redirect("dashboard")

    return render(request, "accounts/set_pin.html")


@login_required
def dashboard(request):
    account = Account.objects.get(user=request.user)
    return render(request, "accounts/dashboard.html", {"account": account})

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "registration/signup.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "registration/signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)
        return redirect("set_pin")

    return render(request, "registration/signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request, "registration/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "registration/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")
