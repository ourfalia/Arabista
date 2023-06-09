from allauth.account.signals import user_signed_up, user_logged_in
from django.db import models
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    try:
        # Check if UserProfile already exists
        user_profile = UserProfile.objects.get(user=instance)
    except UserProfile.DoesNotExist:
        # Create a new UserProfile
        UserProfile.objects.create(user=instance)
    else:
        # Existing UserProfile: just save it
        user_profile.save()
