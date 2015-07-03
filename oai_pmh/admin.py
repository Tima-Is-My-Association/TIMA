from django.contrib import admin
from django.forms import TextInput
from oai_pmh.models import Header, ResumptionToken, TextFieldSingleLine

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
    ]

admin.site.register(Header, HeaderAdmin)
admin.site.register(ResumptionToken, ResumptionTokenAdmin)
