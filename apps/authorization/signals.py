from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=Token)
def set_user_last_login(instance, created, **kwargs):
    if created:
        instance.user.last_login = timezone.now()
        instance.user.save()
