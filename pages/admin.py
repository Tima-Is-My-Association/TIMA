from django.contrib import admin
from django.forms import TextInput
from django.db import models
from pages.models import Page, TextFieldSingleLine

class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)
    readonly_fields = ('slug',)

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['slug', 'title']}),
        ('Text', {'fields': ['text'], 'classes': ('full-width',)}),
    ]

admin.site.register(Page, PageAdmin)