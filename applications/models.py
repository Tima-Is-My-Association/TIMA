from applications.functions.math import get_random_64bit
from django.conf import settings
from django.db import models
from os import urandom

class TextFieldSingleLine(models.TextField):
    pass

class Application(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    name = TextFieldSingleLine(unique=True)
    client_id = TextFieldSingleLine(unique=True)
    secret = TextFieldSingleLine(unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.client_id = ''.join('%02x' % i for i in urandom(32))
            self.secret = ''.join('%02x' % i for i in urandom(32))
        super(Application, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class AuthRequest(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('user',)
        unique_together = ('user', 'timestamp')

class AuthedUser(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    token = TextFieldSingleLine(unique=True)
    n = models.BigIntegerField(default=get_random_64bit)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('user',)
