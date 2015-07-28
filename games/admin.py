from django.contrib import admin
from games.models import AssociationChain

class AssociationChainAdmin(admin.ModelAdmin):
    list_display = ('user', 'chain_id', 'word', 'previous')
    search_fields = ('word__name', 'user__username', 'chain_id')

    fieldsets = [
        (None, {'fields': ['user', 'chain_id', 'word', 'previous']}),
    ]

admin.site.register(AssociationChain, AssociationChainAdmin)
