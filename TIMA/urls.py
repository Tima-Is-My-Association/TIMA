from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'association.views.home', name='home'),
    url(r'^(?P<slug>[\w-]+)/association$', 'association.views.association', name='association'),

    url(r'^signin/$', 'app.views.signin', name='signin'),
    url(r'^signout/$', 'django.contrib.auth.views.logout', name='signout'),
    url(r'^signup/$', 'app.views.signup', name='signup'),
    url(r'^admin/', include(admin.site.urls)),
]