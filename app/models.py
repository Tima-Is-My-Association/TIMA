from association.models import Association, Language
from django.conf import settings
from django.db import models

class TextFieldSingleLine(models.TextField):
    pass

class Profile(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    cultural_background = TextFieldSingleLine(null=True, blank=True)
    languages = models.ManyToManyField(Language, related_name='users')
    points = models.FloatField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('user',)

class AssociationHistory(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    association = models.ForeignKey(Association)
    points = models.FloatField(default=0)

    def __str__(self):
        return '%s - %s' % (self.user, self.association)

    class Meta:
        ordering = ('user',)
