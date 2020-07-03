from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.content, name="content"),
    path("edit/<str:title>", views.edit, name="edit")
]
