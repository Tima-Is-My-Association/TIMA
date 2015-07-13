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
