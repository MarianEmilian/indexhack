import requests
import json

from datetime import datetime, timedelta

from main.models import Article, Company

MOOD = "http://127.0.0.1:4200/mood"
SENTIMENT = "http://127.0.0.1:4200/sentiment"

def get_mood(company):
    company_id = Company.objects.get(name=company)

    articles = Article.objects.filter(company_id=company_id)[0:3].values('headline', 'paragraphs', 'clicks', 'date')
    
    response = requests.get(MOOD, {'articles' : json.dumps(list(articles))})
    
    if response.json()['status_code'] == 200:
        return response.json()['mood']
    else: 
        return 'default'


def get_price(company_name):

    time_threshold = datetime.now() - timedelta(hours=1)
    company = Company.objects.filter(updated_at__lt=time_threshold, name=company_name)
    print(company)
    if company:
        url = 'https://www.forbes.com/search/?q=' + company_name
        response = requests.get(url)
        if response.status_code == 200:
            length = len("<div class=\"entity-stats__price\">")
            start_div = response.text.find("<div class=\"entity-stats__price\"") + length
            end_div = response.text[start_div:].find("</div>")
            price_div = response.text[start_div: start_div + end_div]
            company.update(price = price_div)
            company.update(updated_at= datetime.now())
            return price_div
    else:
        company = Company.objects.get(name=company_name)
        return company.price

def get_sentiment(article):

    response = requests.get(SENTIMENT, {'article' : article})

    if response.json()['status_code'] == 200:
        return response.json()['sentiment']
    else:
         return 'default'