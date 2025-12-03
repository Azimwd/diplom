from rest_framework.permissions import BasePermission
from django.utils.timezone import now
from .models import Subscription

class HasActiveSubscriptionOrOwner(BasePermission):
    message = "У вас нет активной подписки."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if getattr(request.user, 'role', 'user') not in ['lawyer', 'advocate']:
            return True

        sub = (
            Subscription.objects
            .filter(user=request.user, end_date__gt=now())
            .order_by("-end_date")
            .first()
        )
        return sub is not None and sub.is_active

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if obj.user == request.user:
            return True

        if getattr(request.user, 'role', 'user') not in ['lawyer', 'advocate']:
            return True

        sub = (
            Subscription.objects
            .filter(user=request.user, end_date__gt=now())
            .order_by("-end_date")
            .first()
        )
        return sub is not None and sub.is_active

