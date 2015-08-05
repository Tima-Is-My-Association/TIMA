from association.models import Word
from django.db import models
from django.db.models import Max
from django.conf import settings

def default_chain_id():
    chain_id__max = AssociationChain.objects.aggregate(Max('chain_id'))['chain_id__max']
    return chain_id__max + 1 if chain_id__max else 1

class AssociationChain(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    word = models.ForeignKey(Word)
    previous = models.ForeignKey('AssociationChain', blank=True, null=True)
    chain_id = models.PositiveIntegerField(default=default_chain_id)

    def __str__(self):
        return '%s-%s' % (self.chain_id, self.id)

    class Meta:
        ordering = ('chain_id', 'id')
