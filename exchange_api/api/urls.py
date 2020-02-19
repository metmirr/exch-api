from django.urls import path

from . import views

urlpatterns = [
    path("rate", views.rate, name="rate"),
    path("bar", views.best_available_rate, name="best_available_rate"),
]

