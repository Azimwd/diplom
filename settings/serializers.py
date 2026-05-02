from attr import fields
from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import Users
from settings.models import Settings

Users = get_user_model()

class SetSetingsSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Settings
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, attrs):
        unknown_fields = set(self.initial_data.keys()) - set(self.fields.keys())
        if unknown_fields:
            raise serializers.ValidationError(f"Неизвестные поля: {', '.join(unknown_fields)}")
        return super().validate(attrs)
