from django.contrib import admin
from django.forms import TextInput
from oai_pmh.models import Header, TextFieldSingleLine

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

admin.site.register(Header, HeaderAdmin)
