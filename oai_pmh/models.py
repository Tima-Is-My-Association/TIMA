from django.db import models

class TextFieldSingleLine(models.TextField):
    pass

class Header(models.Model):
    identifier = TextFieldSingleLine()
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.identifier

    class Meta:
        ordering = ('identifier',)
