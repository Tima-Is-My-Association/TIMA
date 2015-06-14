from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'association.views.home', name='home'),
    url(r'^(?P<slug>[\w-]+)/association$', 'association.views.association', name='association'),
    url(r'^admin/', include(admin.site.urls)),
]