from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from wuska import settings
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = patterns('wuska.hockey.views',
                       (r'^$', 'index'),   
                       (r'^(?i)index/','index'),
                       (r'^(?i)profile/','profileRedirect'),
                       (r'^(?i)users/(?P<user_id>\d+)/$','profile'),
                       (r'^(?i)freeAgents/$','viewFreeAgentsRedirect'), 
                       (r'^(?i)freeAgents/(?P<position>\w+)/$','viewFreeAgentsRedirect2'), 
                       (r'^(?i)freeAgents/(?P<position>\w+)/(?P<number>\d+)/$','viewFreeAgents'),                      
                       (r'^(?i)allPlayers/$','viewAllPlayersRedirect'), 
                       (r'^(?i)allPlayers/(?P<position>\w+)/$','viewAllPlayersRedirect2'),       
                       (r'^(?i)allPlayers/(?P<position>\w+)/(?P<number>\d+)/$','viewAllPlayers'),         
                       (r'^(?i)allTeams/(?P<number>\d+)/$','viewAllTeams'), 
                       (r'^(?i)allUsers/(?P<number>\d+)/$','viewAllUsers'), 
                       (r'^(?i)users/(?P<user_id>\d+)/viewMessages/$', 'userViewMessagesRedirect'),
                       (r'^(?i)users/(?P<user_id>\d+)/viewMessages/(?P<sent_or_rec>\w+)/(?P<last_message>\d+)/$', 'userViewMessages'),
                       )

urlpatterns += patterns('wuska.hockey.playerView',
                        (r'^(?i)player/(?P<player_id>\d+)/$', 'viewPlayer'),
                        (r'^(?i)player/(?P<player_id>\d+)/upgradeSkill/$', 'upgradeSkill'),
                        (r'^(?i)player/(?P<player_id>\d+)/viewContracts/$', 'viewContracts'),
                        (r'^(?i)player/(?P<player_id>\d+)/buyEquipment/$', 'buyEquipment'),
                        (r'^(?i)createPlayer/','createPlayer'),
                        (r'^(?i)player/(?P<player_id>\d+)/messagePlayer/$', 'messagePlayer'),
                        )

urlpatterns += patterns('wuska.hockey.teamView',
                        (r'^(?i)team/(?P<team_id>\d+)/$', 'viewTeam'),
                        (r'^(?i)createTeam/','createTeam'),
                        (r'^(?i)player/(?P<player_id>\d+)/offerContract/$', 'offerPlayerContract'),
                        (r'^(?i)team/(?P<team_id>\d+)/viewContracts/$', 'viewContracts'),
                        (r'^(?i)team/(?P<team_id>\d+)/editLines/$', 'editLines'),
                        (r'^(?i)team/(?P<team_id>\d+)/messageTeam/$', 'message_team_management'),
                        (r'^(?i)team/(?P<team_id>\d+)/messagePlayersOnTeam/$', 'message_players_on_team'),
                        (r'^(?i)team/(?P<team_id>\d+)/messagePlayers/$', 'message_players_on_team'),
                        (r'^(?i)team/(?P<team_id>\d+)/messageTeamManagement/$', 'message_team_management'),
                        (r'^(?i)team/(?P<team_id>\d+)/viewManagement/$', 'viewManagement'),
                        (r'^(?i)team/(?P<team_id>\d+)/schedule/$', 'viewSchedule'),
                        )

urlpatterns += patterns('wuska.league.views',
                        (r'^(?i)league/(?P<league_id>\d+)/$', 'viewLeague'),
                        (r'^(?i)adminActions/scheduleNewSeason/$', 'scheduleNewSeason'),
                        (r'^(?i)league/(?P<league_id>\d+)/viewSchedule/$', 'viewSchedule'),
                        )

urlpatterns += patterns('',
                        (r'^admin/', include(admin.site.urls)),
                        (r'^accounts/', include('registration.backends.simple.urls')),
                        (r'^(?i)users/(?P<username>\w+)/$','wuska.hockey.views.registration_complete_simple'),
                        )
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
                            )

#urlpatterns += patterns('',
#                     (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }),)

urlpatterns += staticfiles_urlpatterns()
