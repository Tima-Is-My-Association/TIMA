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
    def get_queryset(self, request):
        return Word.objects.annotate(association_count=Count('word'))

    def association_count(self, inst):
        return inst.association_count

    list_display = ('name', 'count', 'language', 'association_count')
    list_filter = ('language',)
    search_fields = ('name',)
    association_count.admin_order_field = 'association_count'
    association_count.short_description = 'Number of Associations'

    formfield_overrides = {
        TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
    }

    fieldsets = [
        (None, {'fields': ['name', 'count', 'language']}),
    ]

class AssociationAdmin(admin.ModelAdmin):
    list_display = ('word', 'association', 'count')
    list_filter = ('word__language', 'count')
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
