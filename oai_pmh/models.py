from django.db import models

class TextFieldSingleLine(models.TextField):
    pass

class Header(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    identifier = TextFieldSingleLine()
    timestamp = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.identifier

    class Meta:
        ordering = ('identifier',)

class ResumptionToken(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    expiration_date = models.DateTimeField()
    complete_list_size = models.IntegerField(default=0)
    cursor = models.IntegerField(default=0)
    token = TextFieldSingleLine()

    def __str__(self):
        return self.token

    class Meta:
        ordering = ('expiration_date',)
