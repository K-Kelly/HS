from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from wuska import settings
admin.autodiscover()

urlpatterns = patterns('hockey.views',
                       (r'^$', 'index'),
                       (r'^player/(?P<player_id>\d+)/$', 'viewPlayer'),
                       (r'^player/(?P<player_id>\d+)/upgradeSkill/$', 'upgradeSkill'),
                       (r'^createPlayer/','createPlayer'),
                       (r'^creatingPlayer/','creatingPlayer'),
                       (r'^team/(?P<team_id>\d+)/$', 'viewTeam'),
                       (r'^createTeam/','createTeam'),
                       (r'^profile/','profile'),
)

urlpatterns += patterns('',
     (r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('registration.urls')),
)

urlpatterns += patterns('',
                        (r'^assets/(?P<path>.*)$', 'django.views.static.serve',{'document_root':     settings.MEDIA_ROOT}),)
