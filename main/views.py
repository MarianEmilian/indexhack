from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Company, User


# Create your views here.

def index(response):
    return render(response, "main/base.html", {})


def home(response):
    return render(response, "main/home.html", {})


def profile(response):
    if response.user.is_authenticated:
        my_dict = {
            'name': '',
            'companies': None
        }
        user = User.objects.get(id=response.user.id)
        my_dict['name'] = user.username
        companies = [x.company.name for x in user.preference_set.all()]
        my_dict['companies'] = companies
        return render(response, "main/profile.html", my_dict)
    else:
        response = redirect('/login')
        return response
