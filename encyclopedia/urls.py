from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>/", views.get_page, name="page"),
    path("wiki/search", views.query_search, name="search")
]
