from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Company, User, Preference
from .forms import PreferenceCreationForm

# Create your views here.

def index(response):
    return render(response, "main/base.html", {})


def home(response):
    return render(response, "main/home.html", {})


def profile(response):
    if response.method =="GET":
        if response.user.is_authenticated:
            my_dict = {
                'name': '',
                'selected_companies': None,
                'form' : None,
            }
            user = User.objects.get(id=response.user.id)
            my_dict['name'] = user.username
            companies = [x.company.name for x in user.preference_set.all()]
            my_dict['selected_companies'] = companies
            form = PreferenceCreationForm(user_id=response.user.id)
            my_dict['form'] = form

            return render(response, "main/profile.html", my_dict)
        else:
            response = redirect('/login')
            return response
    elif response.method == "POST":
        user = User.objects.get(id=response.user.id)
        company = Company.objects.get(id=response.POST['company'])
        preference = Preference(user = user, company = company)
        preference.save()
        return redirect("/watchlist")

def remove_company(response, company):
    user = User.objects.get(id=response.user.id)
    company_id = Company.objects.get(name=company)
    preference = Preference.objects.all().filter(user=user, company=company_id)
    preference.delete()
    return redirect("/watchlist")
