from django.urls import path
from .views import *

urlpatterns = [
    path("", login),
    path("home", main),
    path("register", register),
]