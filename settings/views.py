from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from settings.models import Settings
from settings.serializers import SetSetingsSerializer


class SetSttingsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = SetSetingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                **serializer.data,
                "message": "Настройки успешно применены"
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Ошибка валидации данных"
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            settings_obj = get_object_or_404(Settings, pk=pk)
            serializer = SetSetingsSerializer(settings_obj)
            return Response({
                **serializer.data,
                "message": "Настройки успешно получены"
            }, status=status.HTTP_200_OK)

        settings_obj = Settings.objects.all()
        serializer = SetSetingsSerializer(settings_obj, many=True)
        return Response({
            **serializer.data,
            "message": "Список настроек успешно получен"
        }, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        settings_obj = get_object_or_404(Settings, pk=pk)
        serializer = SetSetingsSerializer(settings_obj, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                **serializer.data,
                "message": "Настройки успешно обновлены"
            }, status=status.HTTP_200_OK)
        return Response({
            **serializer.errors,
            "message": "Ошибка валидации данных"
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        settings_obj = get_object_or_404(Settings, pk=pk)
        serializer = SetSetingsSerializer(settings_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                **serializer.data,
                "message": "Настройки успешно обновлены"
            }, status=status.HTTP_200_OK)
        return Response({
            **serializer.errors,
            "message": "Ошибка валидации данных"
        }, status=status.HTTP_400_BAD_REQUEST)
