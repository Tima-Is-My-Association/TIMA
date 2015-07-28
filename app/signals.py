from app.models import ExcludeWord
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

@receiver(pre_save, sender=ExcludeWord)
def delete_old_exclude_words(sender, **kwargs):
    ExcludeWord.objects.filter(updated_at__lte=(timezone.now() - timezone.timedelta(days=7))).delete()
