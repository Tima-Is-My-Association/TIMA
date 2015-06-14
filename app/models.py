from django.contrib.auth.models import User
from django.db import models

class TextFieldSingleLine(models.TextField):
    pass

class Profile(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User)
    cultural_background = TextFieldSingleLine(null=True, blank=True)
    points = models.FloatField(default=0)

    def __str__(self):
        return self.user

    class Meta:
        ordering = ('user',)