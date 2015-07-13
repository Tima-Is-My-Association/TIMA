from applications.models import Application, TextFieldSingleLine
from django.contrib import admin
from django.forms import TextInput

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_id', 'secret', 'updated_at')
    readonly_fields = ('client_id', 'secret')
    search_fields = ('name',)

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['name', 'client_id', 'secret']}),
    ]

admin.site.register(Application, ApplicationAdmin)
