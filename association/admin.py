from association.models import Association, Language, Word, TextFieldSingleLine
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

    def get_queryset(self, request):
        return Word.objects.annotate(association_count=Count('word'))

    def association_count(self, inst):
        return inst.association_count

    list_display = ('name', 'count', 'get_languages', 'association_count')
    list_filter = ('languages',)
    search_fields = ('name',)
    association_count.admin_order_field = 'association_count'
    association_count.short_description = 'Number of Associations'
    get_languages.short_description = 'Languages'

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['name', 'count', 'languages']}),
    ]

    filter_horizontal = ('languages',)

class AssociationAdmin(admin.ModelAdmin):
    list_display = ('word', 'association', 'count')
    list_filter = ('word__languages', 'count')
    search_fields = ('word__name', 'association__name')

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['word', 'association', 'count']}),
    ]

admin.site.register(Association, AssociationAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Word, WordAdmin)