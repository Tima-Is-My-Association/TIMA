from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from applications.models import AuthedUser, AuthRequest

@receiver(pre_save, sender=AuthRequest)
def delete_old_auth_requests(sender, **kwargs):
    AuthRequest.objects.filter(timestamp__lte=(timezone.now() - timezone.timedelta(minutes=5))).delete()

@receiver(pre_save, sender=AuthRequest)
def delete_old_authed_users(sender, **kwargs):
    AuthedUser.objects.filter(updated_at__lte=(timezone.now() - timezone.timedelta(hours=1))).delete()
