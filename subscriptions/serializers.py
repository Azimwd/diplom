from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "plan", "start_date", "end_date", "is_active"]
        read_only_fields = ["start_date", "end_date", "is_active"]
