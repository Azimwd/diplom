from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import Users
from user_profile.models import Profile
from settings.models import Settings
from allauth.account.signals import user_signed_up
from allauth.account.signals import user_logged_in
from rest_framework_simplejwt.tokens import RefreshToken
@receiver(user_signed_up)
def populate_user_from_google(sender, request, user, sociallogin=None, **kwargs):
    if sociallogin and sociallogin.account.provider == 'google':
        data = sociallogin.account.extra_data

        user.email = data.get('email', '')
        user.save()

        profile, created = Profile.objects.get_or_create(user=user)
        profile.first_name = data.get('given_name', '')
        profile.last_name = data.get('family_name', '')
        profile.email = user.email
        profile.save()
@receiver(user_logged_in)
def set_jwt_cookie(sender, request, user, **kwargs):
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)
    refresh_token = str(refresh)

    request._jwt_access_token = access
    request._jwt_refresh_token = refresh_token
    request._jwt_redirect_url = "http://localhost:4173/chat"
@receiver(post_save, sender=Users)
def create_user_related_data(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Settings.objects.create(user=instance)
