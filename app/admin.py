from app.models import AssociationHistory, Profile, Newsletter, TextFieldSingleLine
from django.contrib import admin
from django.db.models import Count
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
    list_filter = ('user', 'association__word__language', 'association__word', 'association__association')
    search_fields = ('user__username', 'association__word__name', 'association__association__name')

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['user', 'association', 'points']}),
    ]

class NewsletterAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Newsletter.objects.annotate(word_count=Count('words'))

    def word_count(self, inst):
        return inst.word_count

    list_display = ('user', 'word_count', 'updated_at')
    list_filter = ('user', 'words__language', 'words')
    search_fields = ('user__username', 'word__name')
    word_count.admin_order_field = 'word_count'
    word_count.short_description = 'Number of Words'

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['user', 'words']}),
    ]

    filter_horizontal = ('words',)

admin.site.register(AssociationHistory, AssociationHistoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
