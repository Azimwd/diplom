from attr import fields
from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import Users
from settings.models import Settings

Users = get_user_model()

class SetSttingsSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Settings
        fields = "__all__"
        read_only_fields = ["user"]

    