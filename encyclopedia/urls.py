from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.homepage, name="homepage"), 
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>/", views.get_wiki, name="wiki"),
    path("search", views.wiki_search, name="wiki_search"),
    path("new/", views.add_wiki, name="add_wiki"),
    path("edit/<str:title>/", views.edit_wiki, name="edit_wiki"),
    path("delete/<str:title>/", views.delete_wiki, name="delete_wiki"),
    path("random/", views.random_wiki, name="random_wiki")
]