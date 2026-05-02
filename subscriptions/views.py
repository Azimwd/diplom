from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Subscription
from .serializers import SubscriptionSerializer
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import F

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SubscriptionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        active_sub = (
            Subscription.objects
            .filter(user=request.user, end_date__gt=now())
            .order_by("-end_date")
            .first()
        )

        return Response({
            "is_active": active_sub is not None,
            "subscription": {
                "id": active_sub.id if active_sub else None,
                "plan": active_sub.plan if active_sub else None,
                "end_date": active_sub.end_date if active_sub else None
            } if active_sub else None,
            "message": "Подписка проверена"
        })