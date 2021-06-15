from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("watchlist", views.profile, name="home"),
    path("remove/<str:company>", views.remove_company, name="remove company"),
    path("<str:sentiment>", views.view_sorted_sentiment, name="articles")
]
