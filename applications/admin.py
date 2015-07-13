from applications.models import Application, AuthedUser, AuthRequest, TextFieldSingleLine
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

class AuthRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'updated_at')
    list_filters = ('timestamp',)
    search_fields = ('name',)

    fieldsets = [
        (None, {'fields': ['user', 'timestamp']}),
    ]

class AuthedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'n', 'updated_at')
    readonly_fields = ('n', 'token')
    search_fields = ('name',)

    fieldsets = [
        (None, {'fields': ['user', 'token', 'n']}),
    ]

admin.site.register(Application, ApplicationAdmin)
admin.site.register(AuthedUser, AuthedUserAdmin)
admin.site.register(AuthRequest, AuthRequestAdmin)
