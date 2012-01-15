from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from wuska import settings
admin.autodiscover()

urlpatterns = patterns('hockey.views',
                       (r'^$', 'index'),
                       (r'^(?i)player/(?P<player_id>\d+)/$', 'viewPlayer'),
                       (r'^(?i)player/(?P<player_id>\d+)/upgradeSkill/$', 'upgradeSkill'),
                       (r'^(?i)player/(?P<player_id>\d+)/viewContracts/$', 'viewContracts'),
                       (r'^(?i)player/(?P<player_id>\d+)/viewMessages/$', 'viewMessages'),
                       (r'^(?i)player/(?P<player_id>\d+)/buyEquipment/$', 'buyEquipment'),
                       (r'^(?i)player/(?P<player_id>\d+)/offerContract/$', 'offerPlayerContract'),
                       (r'^(?i)player/(?P<player_id>\d+)/messagePlayer/$', 'messagePlayer'),
                       (r'^(?i)createPlayer/','createPlayer'),
                       (r'^(?i)creatingPlayer/','creatingPlayer'),
                       (r'^(?i)team/(?P<team_id>\d+)/$', 'viewTeam'),
                       (r'^(?i)createTeam/','createTeam'),
                       (r'^(?i)profile/','profile'),
)

urlpatterns += patterns('',
     (r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('registration.urls')),
)

urlpatterns += patterns('',
                        (r'^assets/(?P<path>.*)$', 'django.views.static.serve',{'document_root':     settings.MEDIA_ROOT}),)
