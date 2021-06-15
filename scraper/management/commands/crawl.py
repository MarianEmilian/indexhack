from django.core.management.base import BaseCommand
from scraper.scraper.spiders.news_spider import NewsSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

import os
import sys

import datetime as dt


os.chdir("scraper")


def crawl_job():
    settings = get_project_settings()
    process = CrawlerProcess(settings=settings)
    
    os.system("scrapy crawl news")
    return  process.crawl(news_spider.NewsSpider)


def next_crawl(null, hour, min):
    tomorrow = (
        dt.datetime.now() + dt.timedelta(days=1)
        ).replace(hour=hour, minute=minute, second=0, microsecond=0)

    sleep = (tomorrow - dt.datetime.now()).total_seconds()

    reactor.callLater(sleep, crawl)


def crawl():
    cr = crawl_job()
    cr.addCallback(next_crawl, hour = 20, min = 10)
    cr.addErrback(catch_error)

def catch_error(failure):
    print(failure.value)

class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        crawl()
        reactor.run()