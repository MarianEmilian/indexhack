from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Company, User, Preference, Article
from .forms import PreferenceCreationForm
from .utils import get_mood
import requests
from datetime import datetime, timedelta




# Create your views here.
def get_price(company_name):

    time_threshold = datetime.now() - timedelta(hours=1)
    company = Company.objects.filter(updated_at__lt=time_threshold, name=company_name)[0]
    if company:
        return company.price
    else:
        url = 'https://www.forbes.com/search/?q=' + company
        response = requests.get(url)
        if response.status_code == 200:
            length = len("<div class=\"entity-stats__price\">")
            start_div = response.text.find("<div class=\"entity-stats__price\"") + length
            end_div = response.text[start_div:].find("</div>")
            price_div = response.text[start_div: start_div + end_div]
            company.update(price = price_div)
            return price_div
    
def index(response):
    return render(response, "main/base.html", {})


def home(response):
    if response.method == "GET":
        my_dict = {
                'articles': None,
            }
        articles = Article.objects.all()
        

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
            mood_p_company = []
            price_list = []
            for company in companies:
                mood = get_mood(company)
                if mood == 'default':
                    mood_p_company.append('Server Error')
                elif mood > 0:
                    mood_p_company.append('Upward')
                else:
                    mood_p_company.append('Downward')
               
                price_list.append(get_price(company))

            
            my_dict['selected_companies'] =zip(companies, mood_p_company, price_list) 
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
