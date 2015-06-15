from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'association.views.home', name='home'),
    url(r'^(?P<slug>[\w-]+)/association$', 'association.views.association', name='association'),

    url(r'^login/$', 'app.views.ulogin', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
]