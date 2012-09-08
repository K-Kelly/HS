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


class GameAdmin(admin.ModelAdmin):
    list_display = ['id','home_team','home_goals_scored','away_team','away_goals_scored','datetime','has_started','is_completed','is_playoff']
    search_fields = ['id','home_team','away_team','datetime','has_started','is_completed','is_playoff']
    def home_goals_scored(self,obj):
        return obj.home_goals.count()
    home_goals_scored.short_description = 'Home Goals'
    def away_goals_scored(self,obj):
        return obj.away_goals.count()
    away_goals_scored.short_description = 'Away Goals'
admin.site.register(Game,GameAdmin)

class PlayerGameAdmin(admin.ModelAdmin):
    list_display = ['id','player_id','game']
    search_fields = ['id','player_id','game']
admin.site.register(PlayerGame,PlayerGameAdmin)

class GoalAdmin(admin.ModelAdmin):
    list_display = ['id','scorer_id','team_id','primary_assist_id','secondary_assist_id','game']
    search_fields = ['id','scorer_id','team_id','primary_assist_id','secondary_assist_id','game']
admin.site.register(Goal,GoalAdmin)

class PenaltyAdmin(admin.ModelAdmin):
    list_display = ['id','player','team_id','game']
    search_fields = ['id','player','team_id','game','description']
admin.site.register(Penalty,PenaltyAdmin)

