from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status, permissions
from user_profile.serializers import ProfileSerializer
from user_profile.models import Profile

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save(user=request.user)
            return Response({
                "statusCode": 201,
                "success": True,
                "data": serializer.data,
                "message": "Профиль успешно создан"
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "statusCode": 400,
            "success": False,
            "errors": serializer.errors,
            "message": "Ошибка валидации данных"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk = None):
        if pk:
            try:
                profile = Profile.objects.get(pk=pk)
            except Profile.DoesNotExist:
                return Response({
                    "statusCode": 404,
                    "success": False,
                    "data": None,
                    "message": "Профиль не найден"
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProfileSerializer(profile)
            return Response({
                "statusCode": 200,
                "success": True,
                "data": serializer.data,
                "message": "Профиль успешно получен"
            }, status=status.HTTP_200_OK)
        
        profiles  = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response({
                "statusCode": 201,
                "success": True,
                "data": serializer.data,
                "message": "Профиль успешно создан"
            }, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({
                "statusCode": 404,
                "success": False,
                "message": "Профиль не найден"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "statusCode": 200,
                "success": True,
                "data": serializer.data,
                "message": "Профиль успешно обновлён"
            }, status=status.HTTP_200_OK)

        return Response({
            "statusCode": 400,
            "success": False,
            "errors": serializer.errors,
            "message": "Ошибка валидации данных"
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({
                "statusCode": 404,
                "success": False,
                "message": "Профиль не найден"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "statusCode": 200,
                "success": True,
                "data": serializer.data,
                "message": "Профиль частично обновлён"
            }, status=status.HTTP_200_OK)

        return Response({
            "statusCode": 400,
            "success": False,
            "errors": serializer.errors,
            "message": "Ошибка при обновлении профиля"
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({
                "statusCode": 404,
                "success": False,
                "message": "Профиль не найден"
            }, status=status.HTTP_404_NOT_FOUND)

        profile.delete()
        return Response({
            "statusCode": 204,
            "success": True,
            "message": "Профиль успешно удалён"
        }, status=status.HTTP_204_NO_CONTENT)

