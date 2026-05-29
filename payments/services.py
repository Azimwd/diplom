import hashlib
import urllib.parse
from decimal import Decimal
from datetime import timedelta

from django.conf import settings

from .models import Payment
from .utils import generate_unique_invoice_id


SUBSCRIPTION_PLANS = {
    "1m": {
        "title": "1 месяц",
        "amount": Decimal("10000.00"),
        "duration": timedelta(days=30),
    },
    "6m": {
        "title": "6 месяцев",
        "amount": Decimal("50000.00"),
        "duration": timedelta(days=180),
    },
    "1y": {
        "title": "1 год",
        "amount": Decimal("90000.00"),
        "duration": timedelta(days=365),
    },
}


def create_subscription_payment(user, plan):
    if plan not in SUBSCRIPTION_PLANS:
        raise ValueError("Invalid subscription plan")

    plan_data = SUBSCRIPTION_PLANS[plan]

    payment = Payment.objects.create(
        payer=user,
        receiver=None,
        amount=plan_data["amount"],
        invoice_id=generate_unique_invoice_id(),
        purpose="subscription",
        plan=plan,
    )

    return payment


def build_robokassa_url(payment, email=None):
    login = settings.ROBOKASSA_LOGIN
    password1 = settings.ROBOKASSA_PASSWORD1

    amount = Decimal(payment.amount).quantize(Decimal("0.01"))

    desc = f"Оплата подписки Lawly №{payment.invoice_id}"
    desc_encoded = urllib.parse.quote(desc)

    signature = f"{login}:{amount:.2f}:{payment.invoice_id}:{password1}"
    signature_hash = hashlib.md5(signature.encode("utf-8")).hexdigest()

    url = (
        f"https://auth.robokassa.kz/Merchant/Index.aspx?"
        f"MerchantLogin={login}"
        f"&OutSum={amount:.2f}"
        f"&InvId={payment.invoice_id}"
        f"&Description={desc_encoded}"
        f"&SignatureValue={signature_hash}"
        f"&IsTest=1"
    )

    if email:
        url += f"&Email={urllib.parse.quote(email)}"

    return url


def get_subscription_plans_for_response():
    return [
        {
            "plan": plan,
            "title": data["title"],
            "amount": str(data["amount"]),
        }
        for plan, data in SUBSCRIPTION_PLANS.items()
    ]