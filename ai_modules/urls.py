from django.contrib import admin
from django.urls import path
from ai_modules.views import *

app_name = "ai_modules"

urlpatterns = [
    path("sessions/<int:session_id>/ask/",AskView.as_view()),

    path("sessions/<int:session_id>/attorney-price/", AttorneyPriceView.as_view()),

    path("sessions/<int:session_id>/article-win-chance/", ArticleWinChanceView.as_view()),
    
    path("sessions/<int:session_id>/top-lawyers/", TopLawyersByArticleView.as_view()),
]