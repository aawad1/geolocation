from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("coordinates/", views.coordinates, name="coordinates"),

]
