from accounts.models import Language, TextFieldSingleLine
from django.contrib import admin
from django.db.models import Count
from django.forms import TextInput

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'updated_at')
    readonly_fields = ('slug',)
    search_fields = ('name', 'code')

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['slug', 'name', 'code']}),
    ]

admin.site.register(Language, LanguageAdmin)