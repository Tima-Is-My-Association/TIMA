"""buecher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'association.views.association.home', name='home'),
    url(r'^languages/(?P<slug>[\w-]+)/association/$', 'association.views.association.association', name='association'),

    url(r'^words/$', 'association.views.words.words', name='words'),
    url(r'^words/(?P<word_id>\d+)/$', 'association.views.words.word', name='word'),

    url(r'^leaderboard/$', 'app.views.leaderboard.leaderboard', name='leaderboard'),
    url(r'^statistics/$', 'app.views.statistics.statistics', name='statistics'),

    url(r'^profile/$', 'app.views.profile.profile', name='profile'),
    url(r'^profile/associationhistory/$', 'app.views.profile.association_history', name='association_history'),
    url(r'^profile/edit/$', 'app.views.profile.edit', name='profile_edit'),
    url(r'^profile/edit/password/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^profile/edit/password/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^profile/newsletter/$', 'app.views.profile.newsletter', name='newsletter'),

    url(r'^pages/faq/$', 'pages.views.faq', name='faq'),
    url(r'^pages/(?P<slug>[\w-]+)/$', 'pages.views.page', name='page'),

    url(r'^signin/$', 'app.views.base.signin', name='signin'),
    url(r'^signout/$', 'django.contrib.auth.views.logout', name='signout'),
    url(r'^signup/$', 'app.views.base.signup', name='signup'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/applications/auth/request/$', 'applications.views.api.auth.request'),
    url(r'^api/applications/auth/user/$', 'applications.views.api.auth.user'),
    url(r'^api/applications/auth/revoke/$', 'applications.views.api.auth.revoke'),
    url(r'^api/languages/$', 'association.views.api.languages.list'),
    url(r'^api/leaderboard/$', 'app.views.api.leaderboard.leaderboard'),
    url(r'^api/profile/$', 'app.views.api.profile.profile'),
    url(r'^api/profile/associationhistory/$', 'app.views.api.profile.associationhistory'),
    url(r'^api/statistics/$', 'app.views.api.statistics.statistics'),
    url(r'^api/association/$', 'association.views.api.associations.association'),
    url(r'^api/words/$', 'association.views.api.words.export', name='words_export'),
    url(r'^api/words/graph/$', 'association.views.api.words.graph', name='word_graph'),
    url(r'^api/words/isa/$', 'association.views.api.words.isA'),
    url(r'^api/words/next/$', 'association.views.api.words.next'),

    url(r'^oai2/$', 'oai_pmh.views.oai2', name='oai2'),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
]
