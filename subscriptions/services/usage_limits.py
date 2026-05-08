from django.db import transaction
from django.utils.timezone import now
from rest_framework.response import Response

from subscriptions.models import Subscription


def has_active_subscription(user):
    return Subscription.objects.filter(
        user=user,
        end_date__gt=now()
    ).exists()


def consume_user_token(user):

    if has_active_subscription(user):
        return None

    with transaction.atomic():
        user = type(user).objects.select_for_update().get(id=user.id)

        if user.freeRequest <= 0:
            return Response(
                {"message": "Нет доступных бесплатных запросов"},
                status=402
            )

        user.freeRequest -= 1
        user.save(update_fields=["freeRequest"])

    return None