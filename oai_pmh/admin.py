from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from oai_pmh.models import DCRecord, Header, MetadataFormat, ResumptionToken, Set, TextFieldSingleLine

class DCRecordAdmin(admin.ModelAdmin):
    list_display = ('dc_identifier', 'dc_title', 'dc_creator')
    list_filter = ('dc_date',)
    readonly_fields = ('dc_date',)
    search_fields = ('dc_identifier', 'dc_title', 'dc_creator', 'dc_subject', 'dc_description', 'dc_publisher', 'dc_contributor', 'dc_date', 'dc_type', 'dc_format', 'dc_identifier', 'dc_source', 'dc_language', 'dc_relation', 'dc_coverage', 'dc_rights')

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['header', 'dc_title', 'dc_creator', 'dc_subject', 'dc_description', 'dc_publisher', 'dc_contributor', 'dc_date', 'dc_type', 'dc_format', 'dc_identifier', 'dc_source', 'dc_language', 'dc_relation', 'dc_coverage', 'dc_rights']}),
    ]

class DCRecordInline(admin.StackedInline):
    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    model = DCRecord

class HeaderAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'timestamp', 'deleted')
    list_filter = ('timestamp', 'deleted')
    readonly_fields = ('timestamp',)
    search_fields = ('identifier',)

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['identifier', 'timestamp', 'deleted']}),
        ('Metadata formats', {'fields': ['metadata_formats']}),
        ('Sets', {'fields': ['sets']}),
    ]

    filter_horizontal = ('metadata_formats', 'sets')
    inlines = [DCRecordInline,]

class MetadataFormatAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'schema', 'namespace')
    search_fields = ('prefix', 'schema', 'namespace')

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['prefix', 'schema', 'namespace']}),
    ]

class ResumptionTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'expiration_date', 'complete_list_size', 'cursor')
    list_filter = ('expiration_date',)
    search_fields = ('token', 'complete_list_size', 'cursor')

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['token', 'expiration_date', 'complete_list_size', 'cursor']}),
        ('Optinal', {'fields': ['from_timestamp', 'until_timestamp', 'metadata_prefix', 'set_spec']}),
    ]

class SetAdmin(admin.ModelAdmin):
    list_display = ('name', 'spec', 'description')
    search_fields = ('name', 'spec', 'description')

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
        models.TextField: {'widget': Textarea(attrs={'autocomplete':'off', 'rows':20, 'style':'width: 100%; resize: none;'})},
    }

    fieldsets = [
        (None, {'fields': ['name', 'spec', 'description']}),
    ]

admin.site.register(DCRecord, DCRecordAdmin)
admin.site.register(Header, HeaderAdmin)
admin.site.register(MetadataFormat, MetadataFormatAdmin)
admin.site.register(ResumptionToken, ResumptionTokenAdmin)
admin.site.register(Set, SetAdmin)
