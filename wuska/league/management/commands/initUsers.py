from django.core.management.base import BaseCommand,CommandError,NoArgsCommand
from wuska.hockey.models import Team,Player,Arena,Tactics,League
from django.contrib.auth.models import User

class Command(NoArgsCommand):
    help = 'Creates initial users, players, and teams. Places players on teams.'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
      

             
    def handle_noargs(self,**options):
        player_id = 1
        user_num = 2
        team_num = 1     
        email = "testUser%s@dkflajsoiwefnwefneocnieaj.com"   
        while user_num <=31:
            user = User.objects.create_user('user%s'%user_num,email%(user_num),'test')
            #create team
            name = "Team%s" % (team_num)
            abbreviation = "T%s" % (team_num)
            arena_name = "Arena%s" % (team_num)
            

            arena = Arena(name=arena_name, occupancy=5000, practice_facility=0,locker_room=0, equipment=0, rink=0, concessions=0, lower_bowl=1, mid_bowl=0, upper_bowl=0, box=0, ticket_lower=5, ticket_mid=2, ticket_upper=1, ticket_box=10)
            arena.save()
            tactics = Tactics()
            tactics.save()
            team = Team(name=name,abbreviation=abbreviation, owner=user.id, general_manager1=-1,general_manager2=-1, league_id=-1,arena=arena,funds=2000000, salary_used=0, salary_left=2000000,numLWNeed=4,numCNeed=4,numRWNeed=4,numDNeed=6,numGNeed=2,avgAge=00.000, contract_status_change=False,division = -1,tactics=tactics)
            team.save()
            user.get_profile().teams_owned.add(team)
            user.get_profile().teams.add(team) 
            num_leagues = League.objects.all().count()
            if num_leagues == 0:
                league = League(name='League 1',salary_cap = 8000000,is_full=False,season_number=-1)
                league.save()
            else:
                league = League.objects.order_by('-pk')[0]
            if league.is_full:#If last created league is full, make new one
                league = League(name='League %s'%(num_leagues + 1),salary_cap = 8000000,is_full=False,season_number=-1)
                league.save()

            num_div1,num_div2,num_div3,num_div4,num_div5,num_div6 = 0,0,0,0,0,0
            for team2 in league.teams.all():
                if team2.division == 1:
                    num_div1 += 1
                elif team2.division == 2:
                    num_div2 += 1
                elif team2.division == 3:
                    num_div3 += 1
                elif team2.division == 4:
                    num_div4 += 1
                elif team2.division == 5:
                    num_div5 += 1
                elif team2.division == 6:
                    num_div6 += 1
                    
            if num_div1 < 5:
                team.division = 1
            elif num_div2 < 5:
                team.division = 2
            elif num_div3 < 5:
                team.division = 3
            elif num_div4 < 5:
                team.division = 4
            elif num_div5 < 5:
                team.division = 5
            elif num_div6 < 5:
                team.division = 6
                num_div6 += 1
                if num_div6  == 5:
                    league.is_full = True
            else:
                raise Exception("League is full when it shouldn't be. Please post on the support page about this issue or notify an admin so that we can quickly fix this issue for you!")                                           
            league.teams.add(team)
            league.save()
            team.league_id = league.id
            team.save()
                    
            #create player
            player_num = 0
            while player_num <= 20:
                player_id += 1
                name = "Player%s" % player_id                
                if player_num <= 4:
                    position = "L"
                elif player_num <= 8:
                    position = "C"
                elif player_num <= 12:
                    position = "R"
                elif player_num <= 18:
                    position = "D"
                else:
                    position = "G"
                height = 70
                weight = 180
                team_id = team.id#free agent
                user_id = user.id 
                upgrades = 10
                level = 1
                experience = 0
                age = 18
                retired = False
                salary = 0
                contract_end = 0
                no_trade = False
                style = 1 # need to make user choose this
                shooting = 1
                passing = 1
                stick_handling = 1
                checking = 1
                positioning = 1
                endurance = 1
                skating = 1
                strength = 1
                faceoff = 1
                fighting = 1
                awareness = 1
                leadership = 1
                helmet = 0
                gloves = 0
                shoulder_pads = 0
                pants = 0
                skates = 0
                stick = 0
                free_agent = True
                player = Player(team_id = team_id, user_id = user_id, upgrades = upgrades, level = level, experience = experience, name = name, age = age, retired = retired, height = height, weight = weight, salary =salary, contract_end = contract_end, no_trade = no_trade, position = position, style = style, shooting = shooting, passing = passing, stick_handling = stick_handling, checking = checking, positioning = positioning, endurance = endurance, skating = skating, strength = strength, faceoff = faceoff, fighting = fighting, awareness = awareness, leadership = leadership, helmet = helmet, gloves = gloves, shoulder_pads = shoulder_pads, pants = pants, skates = skates, stick = stick, free_agent = free_agent,new_contract=False)
                player.save()
                team.players.add(player)
                team.save()
                user.get_profile().players.add(player) 
                user.get_profile().save()
                user.save()
                player_num += 1

            user_num += 1
            team_num += 1
        self.stdout.write('Successfully made %s users, %s teams, %s players'% (user_num,team_num,player_id))

