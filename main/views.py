from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Company, User, Preference, Article
from .forms import PreferenceCreationForm
from .utils import get_mood, get_price, get_sentiment






# Create your views here. 
def index(response):
    return render(response, "main/base.html", {})


def view_sorted_sentiment(response, sentiment):
    if response.method == "GET":
        my_dict = {
                'articles': None,
            }
        headlines= []
        sentiments = []
        urls = []
        articles = Article.objects.all().filter(sentiment = sentiment)
        
        for article in articles:
            headlines.append(article.headline)
            sentiments.append(article.sentiment)
            urls.append(article.url)
        my_dict['articles'] = zip(headlines, sentiments, urls)
    return render(response, "main/home.html", my_dict)


def home(response):
    if response.method == "GET":
        my_dict = {
                'articles': None,
            }
        headlines= []
        sentiments = []
        urls = []
        articles = Article.objects.all()
        
        for article in articles:
            if not article.sentiment:
                sentiment = get_sentiment(article.paragraphs)
                article.sentiment = sentiment
                article.save()

            headlines.append(article.headline)
            sentiments.append(article.sentiment)
            urls.append(article.url)
        my_dict['articles'] = zip(headlines, sentiments, urls)
    return render(response, "main/home.html", my_dict)


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
