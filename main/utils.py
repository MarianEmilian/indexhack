import requests
import json

from main.models import Article, Company

MOOD = "http://127.0.0.1:4200/mood"

def get_mood(company):
    company_id = Company.objects.get(name=company)

    articles = Article.objects.filter(company_id=company_id)[0:3].values('headline', 'paragraphs', 'clicks', 'date')
    
    response = requests.get(MOOD, {'articles' : json.dumps(list(articles))})
    
    if response.json()['status_code'] == 200:
        return response.json()['mood']
    else: 
        return 'default'