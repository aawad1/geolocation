from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("about/", views.about, name="about"),
    path("history/", views.history, name="history"),
]
