# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import sys

sys.path += ["../../"]

from scrapy_djangoitem import DjangoItem
from main.models import Article, Company


class ArticleItem(DjangoItem):
    django_model = Article


class CompanyItem(DjangoItem):
    django_model = Company
