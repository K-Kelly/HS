from django.core.management.base import BaseCommand,CommandError,NoArgsCommand
from wuska.hockey.models import Team,Player
from wuska.accounts.models import UserProfile

class Command(NoArgsCommand):
    help = 'Creates initial players and teams. Places players on teams.'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
    
    def handle_noargs(self,**options):
        player_num = 1
        user_num = 1
        team_num = 1
        
        
        while user_num <=31:
            user = User.objects.create_user('user%s'%user_num,email%(user_num),'test')
            user.save()
            user_num += 1
        self.stdout.write('Successfully made 30 users.')


