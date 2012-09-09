from django.core.management.base import BaseCommand
from game_class import PlayGame
from wuska.hockey.models import Game,Team
from django.shortcuts import get_object_or_404
from django.utils.timezone import utc
from random import randrange
from datetime import datetime,timedelta
from time import strptime,mktime
from itertools import chain
from django.shortcuts import get_object_or_404
from django.utils.timezone import utc
from random import randrange,uniform
from datetime import datetime,timedelta
from itertools import chain
from math import trunc

class Command(BaseCommand):
    help = 'Runs the games for this 15 min period'
    def handle(self,*args, **options):
        run_time_period()
        self.stdout.write("Successfully ran this 15 min period.\n")

def run_time_period():
    #round current time to 15 min increments
    dt = datetime.now()
    start_time = dt - timedelta(minutes=dt.minute % 15,seconds = dt.second, microseconds = dt.microsecond)
    #games_now = Game.objects.filter(datetime = start_time)
    season_number = get_object_or_404(Team,pk=1).seasons.all().count()
    game = get_object_or_404(Game,pk=3)
    games_now = Game.objects.all()
    for game in games_now:
        if not game.has_started:
            pg = PlayGame(game,season_number)
            pg.play_game()
        
