from django.contrib import admin
from django.urls import path
from settings.views import *

app_name = "payments"
urlpatterns = [
    path("", SetSttingsView.as_view()),      
    path("<int:pk>/", SetSttingsView.as_view()),
]
