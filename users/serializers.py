import email
from rest_framework.exceptions  import AuthenticationFailed
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from users.models import Users

Users = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)
    class Meta:
        model = Users

        fields = [
            "id",
            "email",
            "password",
            "confirmPassword",
            "agreementAccepted",
            "privacyPolicyAccepted",
        ]
        read_only_fields = ('id', 'created_at',)

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if not data.get("agreementAccepted"):
            raise serializers.ValidationError("Необходимо принять пользовательское соглашение")
        if not data.get("privacyPolicyAccepted"):
            raise serializers.ValidationError("Необходимо принять условия конфиденциальности")

        if data["password"] != data["confirmPassword"]:
            raise serializers.ValidationError("Пароли не совпадают")
        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return data 
    
    def create(self, validated_data):
        validated_data.pop('confirmPassword')

        user = Users.objects.create_user(   
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user'),
            agreementAccepted=validated_data.get('agreementAccepted', False),
            privacyPolicyAccepted=validated_data.get('privacyPolicyAccepted', False),
            agreementVersion=validated_data.get('agreementVersion'),
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = Users.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise AuthenticationFailed("Неверная почта или пароль")

        return {"user": user}
