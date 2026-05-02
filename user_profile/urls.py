from django.contrib import admin
from django.urls import path
from user_profile.views import *
from rest_framework.routers import DefaultRouter

app_name = "profile"



router = DefaultRouter()
router.register("", ProfileViewSet)

urlpatterns = router.urls
