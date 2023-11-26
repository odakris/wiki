from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.homepage, name="homepage"), 
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>/", views.get_wiki, name="wiki"),
    path("search", views.wiki_search, name="wiki_search"),
    path("add/", views.add_wiki, name="add_wiki"),
    path("wiki/<str:title>/edit", views.edit_wiki, name="edit_wiki")
]
