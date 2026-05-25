from django.urls import path
from .views import (
    CreateSubscriptionInvoiceView,
    GetInvoiceUrlView,
    RobokassaResultView,
    RobokassaSuccessView,
    RobokassaFailView,
)

app_name = "payments"

urlpatterns = [
    path(
        "subscription/create-invoice/",
        CreateSubscriptionInvoiceView.as_view(),
        name="create_subscription_invoice"
    ),

    path(
        "invoice/url/",
        GetInvoiceUrlView.as_view(),
        name="get_invoice_url"
    ),

    path(
        "robokassa/result/",
        RobokassaResultView.as_view(),
        name="robokassa_result"
    ),

    path(
        "robokassa/success/",
        RobokassaSuccessView.as_view(),
        name="robokassa_success"
    ),

    path(
        "robokassa/fail/",
        RobokassaFailView.as_view(),
        name="robokassa_fail"
    ),
]