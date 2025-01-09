from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, raw, created, **kwargs):
    if created:
        if not raw:
            Profile.objects.create(user=instance)   
