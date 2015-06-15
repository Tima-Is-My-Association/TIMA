from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'association.views.home', name='home'),
    url(r'^languages/(?P<slug>[\w-]+)/association$', 'association.views.association', name='association'),

    url(r'^leaderboard/$', 'app.views.leaderboard.leaderboard', name='leaderboard'),

    url(r'^profile/$', 'app.views.profile.profile', name='profile'),
    url(r'^profile/association_history/$', 'app.views.profile.association_history', name='association_history'),

    url(r'^signin/$', 'app.views.base.signin', name='signin'),
    url(r'^signout/$', 'django.contrib.auth.views.logout', name='signout'),
    url(r'^signup/$', 'app.views.base.signup', name='signup'),

    url(r'^admin/', include(admin.site.urls)),
]