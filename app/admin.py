from app.models import AssociationHistory, Profile, TextFieldSingleLine
from django.contrib import admin
from django.forms import TextInput

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cultural_background', 'points')
    search_fields = ('user__username', 'cultural_background')

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['user', 'cultural_background', 'points']}),
    ]

class AssociationHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'association', 'points')
    list_filter = ('user', 'association__word__languages', 'association__word', 'association__association')
    search_fields = ('user__username', 'association__word__name', 'association__association__name')

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['user', 'association', 'points']}),
    ]

admin.site.register(AssociationHistory, AssociationHistoryAdmin)
admin.site.register(Profile, ProfileAdmin)