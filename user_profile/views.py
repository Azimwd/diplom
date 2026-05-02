from rest_framework.permissions import IsAuthenticated
from user_profile.serializers import ProfileSerializer
from user_profile.permissions import IsOwnerProfile
from user_profile.models import Profile
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfile]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

