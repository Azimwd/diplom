from rest_framework.permissions import BasePermission

class IsOwnerProfile(BasePermission):
    message = "Этот профиль вам не принадлежит."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
