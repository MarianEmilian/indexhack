from django.shortcuts import render, redirect
from . import forms as f


# Create your views here.

def register(response):
    if response.method == "POST":
        form = f.RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/accounts/login")
    else:
        form = f.RegisterForm()
    return render(response, "register/registration.html", {"form": form})

