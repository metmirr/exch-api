from django.urls import path

from . import views

urlpatterns = [path("rate", views.rate, name="rate")]

