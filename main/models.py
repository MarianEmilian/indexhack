from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=30)
    price = models.CharField(max_length=20, default=None, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Article(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    headline = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    blog_id = models.CharField(max_length=300)
    paragraphs = models.TextField(blank=True, null=True)
    clicks = models.IntegerField()
    url = models.URLField(default=None)
    sentiment = models.CharField(max_length=12, null=True, blank=True)
    def __str__(self):
        return self.headline


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.company.name
