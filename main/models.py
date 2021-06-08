from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Article(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    headline = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    blog_id = models.CharField(max_length=300)
    paragraphs = models.TextField(blank=True, null=True)
    clicks = models.IntegerField()

    def __str__(self):
        return self.headline


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.company.name
