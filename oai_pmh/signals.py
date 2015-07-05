from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from oai_pmh.models import ResumptionToken

@receiver(pre_save, sender=ResumptionToken)
def delete_old_resumption_tokens(sender, **kwargs):
    ResumptionToken.objects.filter(expiration_date__lte=timezone.now()).delete()
