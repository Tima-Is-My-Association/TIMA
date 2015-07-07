from django.contrib import admin
from django.forms import Textarea, TextInput
from django.db import models
from pages.models import Page, TextFieldSingleLine

class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)
    readonly_fields = ('slug',)

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
        models.TextField: {'widget': Textarea(attrs={'autocomplete':'off', 'rows':20, 'style':'width: 100%; resize: none;'})},
    }

    fieldsets = [
        (None, {'fields': ['slug', 'title']}),
        ('Text', {'fields': ['text']}),
    ]

admin.site.register(Page, PageAdmin)
