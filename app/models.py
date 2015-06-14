from association.models import Association
from django.conf import settings
from django.db import models

class TextFieldSingleLine(models.TextField):
    pass

class Profile(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    cultural_background = TextFieldSingleLine(null=True, blank=True)
    points = models.FloatField(default=0)

    def __str__(self):
        return self.user

    class Meta:
        ordering = ('user',)

class AssociationHistory(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    association = models.ForeignKey(Association)
    points = models.FloatField(default=0)

    def __str__(self):
        return '%s - %s' % (self.user, self.association)

    class Meta:
        ordering = ('user',)