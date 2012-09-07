from wuska.hockey.models import *
from django.contrib import admin

admin.site.register(Player)
admin.site.register(Arena)
admin.site.register(Team)
admin.site.register(Contract)
admin.site.register(Message)
admin.site.register(League)
admin.site.register(PlayerSeason)
admin.site.register(TeamSeason)


admin.site.register(Goal)
admin.site.register(Penalty)

class GameAdmin(admin.ModelAdmin):
    list_display = ['id','home_team','away_team','datetime','has_started','is_completed','is_playoff']
    search_fields = ['id','home_team','away_team','datetime','has_started','is_completed','is_playoff']

admin.site.register(Game,GameAdmin)

class PlayerGameAdmin(admin.ModelAdmin):
    list_display = ['id','player_id','game']
    search_fields = ['id','player_id','game']
admin.site.register(PlayerGame,PlayerGameAdmin)
