from django.contrib import admin
from django.urls import path
from user_profile.views import *

app_name = "profile"

urlpatterns = [
    path("", ProfileView.as_view()),      
    path("<int:pk>/", ProfileView.as_view()),
]