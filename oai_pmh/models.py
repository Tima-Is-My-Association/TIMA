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

class DCRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    header = models.OneToOneField(Header, primary_key=True)
    dc_title = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:title')
    dc_creator = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:creator')
    dc_subject = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:subject')
    dc_description = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:description')
    dc_publisher = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:publisher')
    dc_contributor = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:contributor')
    dc_date = models.DateTimeField(auto_now=True, verbose_name=' dc:date')
    dc_type = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:type')
    dc_format = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:format')
    dc_identifier = TextFieldSingleLine(verbose_name=' dc:identifier')
    dc_source = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:source')
    dc_language = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:language')
    dc_relation = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:relation')
    dc_coverage = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:coverage')
    dc_rights = TextFieldSingleLine(blank=True, null=True, verbose_name=' dc:rights')

    def __str__(self):
        return str(self.header)

    class Meta:
        ordering = ('header',)
        verbose_name = 'Dublin Core record'
