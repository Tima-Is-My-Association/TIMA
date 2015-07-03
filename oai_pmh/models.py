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

class Header(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    identifier = TextFieldSingleLine(unique=True)
    timestamp = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    metadata_formats = models.ManyToManyField(MetadataFormat, related_name='identifiers', blank=True)
    sets = models.ManyToManyField(Set, related_name='headers', blank=True)

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
    token = TextFieldSingleLine(unique=True)

    from_timestamp = models.DateTimeField(blank=True, null=True)
    until_timestamp = models.DateTimeField(blank=True, null=True)
    metadata_prefix = models.ForeignKey(MetadataFormat, blank=True, null=True)
    set_spec = models.ForeignKey(Set, blank=True, null=True)


    def __str__(self):
        return self.token

    class Meta:
        ordering = ('expiration_date',)
