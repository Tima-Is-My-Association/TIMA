from association.models import Language, Word, TextFieldSingleLine
from django.contrib import admin
from django.db.models import Count
from django.forms import TextInput

class LanguageAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Language.objects.annotate(word_count=Count('words'))

    def word_count(self, inst):
        return inst.word_count

    list_display = ('name', 'code', 'word_count')
    readonly_fields = ('slug',)
    search_fields = ('name', 'code')
    word_count.admin_order_field = 'word_count'
    word_count.short_description = 'Number of Words'

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['slug', 'name', 'code']}),
    ]

class WordAdmin(admin.ModelAdmin):
    def get_languages(self, obj):
        return ', '.join([str(language) for language in obj.languages.all()])

    list_display = ('name', 'count', 'get_languages')
    list_filter = ('languages',)
    readonly_fields = ('slug',)
    search_fields = ('name',)
    get_languages.short_description = 'Languages'

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['slug', 'name', 'count', 'languages']}),
    ]

    filter_horizontal = ('languages',)

admin.site.register(Language, LanguageAdmin)
admin.site.register(Word, WordAdmin)