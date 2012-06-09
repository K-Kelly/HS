from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from wuska import settings
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = patterns('hockey.views',
                       (r'^$', 'index'),                      
                       (r'^(?i)profile/','profile'),
                       (r'^(?i)freeAgents/(?P<position>\w+)/$','viewFreeAgents'),
)

urlpatterns += patterns('hockey.playerView',
                        (r'^(?i)player/(?P<player_id>\d+)/$', 'viewPlayer'),
                        (r'^(?i)player/(?P<player_id>\d+)/upgradeSkill/$', 'upgradeSkill'),
                        (r'^(?i)player/(?P<player_id>\d+)/viewContracts/$', 'viewContracts'),
                        (r'^(?i)player/(?P<player_id>\d+)/viewMessages/$', 'viewMessages'),
                        (r'^(?i)player/(?P<player_id>\d+)/buyEquipment/$', 'buyEquipment'),
                        (r'^(?i)createPlayer/','createPlayer'),
                        (r'^(?i)creatingPlayer/','creatingPlayer'),
                        (r'^(?i)player/(?P<player_id>\d+)/messagePlayer/$', 'messagePlayer'),
)

urlpatterns += patterns('hockey.teamView',
                        (r'^(?i)team/(?P<team_id>\d+)/$', 'viewTeam'),
                        (r'^(?i)createTeam/','createTeam'),
                        (r'^(?i)player/(?P<player_id>\d+)/offerContract/$', 'offerPlayerContract'),
                        #(r'^(?i)player/(?P<player_id>\d+)/messagePlayer/$', 'messagePlayer'),
                        (r'^(?i)team/(?P<team_id>\d+)/editLines$', 'editLines'),
                        (r'^(?i)team/(?P<team_id>\d+)/messageTeam$', 'message_players_on_team'),
                        (r'^(?i)team/(?P<team_id>\d+)/messagePlayersOnTeam$', 'message_players_on_team'),
                        (r'^(?i)team/(?P<team_id>\d+)/messagePlayers$', 'message_players_on_team'),
)

urlpatterns += patterns('',
     (r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('registration.backends.default.urls')),

)

urlpatterns += patterns('',
                        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }),)

urlpatterns += staticfiles_urlpatterns()
