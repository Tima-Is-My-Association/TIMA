from django.db import models

class TextFieldSingleLine(models.TextField):
    pass

class MetadataFormat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    prefix = TextFieldSingleLine(unique=True)
    schema = models.URLField(max_length=2048)
    namespace = models.URLField(max_length=2048)

    def __str__(self):
        return self.prefix

    class Meta:
        ordering = ('prefix',)

class Header(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    identifier = TextFieldSingleLine(unique=True)
    timestamp = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    metadata_formats = models.ManyToManyField(MetadataFormat, related_name='identifiers')

    def __str__(self):
        return self.identifier

    class Meta:
        ordering = ('identifier',)

class Set(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    spec = TextFieldSingleLine(unique=True)
    name = TextFieldSingleLine()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

