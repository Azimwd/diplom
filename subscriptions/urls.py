from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, SubscriptionStatusView

app_name = "subscriptions"

router = DefaultRouter()
router.register(r'', SubscriptionViewSet, basename="subscriptions")

urlpatterns = [

    path('status/', SubscriptionStatusView.as_view(), name="subscriptions-status"),
    path('', include(router.urls)),
]
