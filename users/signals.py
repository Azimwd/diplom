from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import Users
from user_profile.models import Profile
from settings.models import Settings


@receiver(post_save, sender=Users)
def create_user_related_data(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Settings.objects.create(user=instance)
