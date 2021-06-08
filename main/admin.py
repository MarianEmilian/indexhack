from django.contrib import admin
from .models import Company, Article, Preference

# Register your models here.


admin.site.register(Company)
admin.site.register(Article)
admin.site.register(Preference)
