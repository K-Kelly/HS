from django.shortcuts import get_object_or_404
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from wuska.hockey.models import *
from django.test.client import Client

class PlayerTest(TestCase): 
    def setUp(self):
        self.client = Client()
        self.client.post('/accounts/register/',{'username':'PlayerTest1', 'email':'test@localhosttestregister.com','password1':'test','password2':'test'},follow=True)        
    
    def test_create_player(self):
        response = self.client.get('/allUsers/25/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'viewAllUsers.html')
        self.assertContains(response,"PlayerTest1")
        #Create Player
        response = self.client.post('/createPlayer/',{'name':'TestPlayer1','position':'L','height':'70','weight':'180'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewPlayer.html')
        response = self.client.get('/Player/1/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewPlayer.html')
        p = get_object_or_404(Player,pk = 1)
        #Compare created player to itself after being retrieved
        self.assertEqual(p.name, "TestPlayer1")
        self.assertEqual(p.team_id, -1)
        self.assertEqual(p.user_id, 2)
        self.assertEqual(p.upgrades, 10)
        self.assertEqual(p.level, 1)
        self.assertEqual(p.experience, 0)
        self.assertEqual(p.age, 18)
        self.assertEqual(p.retired, False)
        self.assertEqual(p.height, 70)
        self.assertEqual(p.weight, 180)
        self.assertEqual(p.salary, 0)
        self.assertEqual(p.contract_end, 0)
        self.assertEqual(p.no_trade, False)
        self.assertEqual(p.position, "L")
        self.assertEqual(p.style, 1)
        self.assertEqual(p.shooting, 1)
        self.assertEqual(p.passing, 1)
        self.assertEqual(p.stick_handling, 1)
        self.assertEqual(p.checking, 1)
        self.assertEqual(p.positioning, 1)
        self.assertEqual(p.endurance, 1)
        self.assertEqual(p.skating, 1)
        self.assertEqual(p.strength, 1)
        self.assertEqual(p.faceoff, 1)
        self.assertEqual(p.fighting, 1)
        self.assertEqual(p.awareness, 1)
        self.assertEqual(p.leadership, 1)
        self.assertEqual(p.helmet, 0)
        self.assertEqual(p.gloves, 0)
        self.assertEqual(p.shoulder_pads, 0)
        self.assertEqual(p.pants, 0)
        self.assertEqual(p.skates, 0)
        self.assertEqual(p.stick, 0)
        self.assertEqual(p.free_agent, True)
        #test Upgrades
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'shooting'},follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'passing'},follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'stick_handling'},follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'checking'},follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'positioning'},follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'endurance'},follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'skating'},follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'strength'},follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'faceoff'},follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'fighting'},follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'awareness'},follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.post('/player/1/upgradeSkill/',{'skill':'leadership'},follow=True)
        self.assertEqual(response.status_code,200)
        p = get_object_or_404(Player,pk = 1)
        self.assertEqual(p.shooting, 2)
        self.assertEqual(p.passing, 2)
        self.assertEqual(p.stick_handling, 2)
        self.assertEqual(p.checking, 2)
        self.assertEqual(p.positioning, 2)
        self.assertEqual(p.endurance, 2)
        self.assertEqual(p.skating, 2)
        self.assertEqual(p.strength, 2)
        self.assertEqual(p.faceoff, 2)
        self.assertEqual(p.fighting, 2)
        self.assertEqual(p.awareness, 1)#10 upgrades used so should still be 1
        self.assertEqual(p.leadership, 1)

        #Create Team
        response = self.client.post('/createTeam/',{'name':'Team1','abbreviation':'TEA','arena_name':'Arena1'},follow=True)
        self.assertEqual(response.status_code,200)
        t = get_object_or_404(Team,name="Team1")
        self.assertEqual(t.name, 'Team1')
        self.assertEqual(t.owner, 2)
        self.assertEqual(t.general_manager1,-1)
        self.assertEqual(t.general_manager2,-1)
        #self.assertEqual(t.league_id,-1)
        self.assertEqual(t.arena.name,'Arena1')
        self.assertEqual(t.funds,2000000)
        self.assertEqual(t.salary_used,0)
        self.assertEqual(t.salary_left,2000000)
        self.assertEqual(t.numLWNeed,4)
        self.assertEqual(t.numCNeed,4)
        self.assertEqual(t.numRWNeed,4)
        self.assertEqual(t.numDNeed,6)
        self.assertEqual(t.numGNeed,2)
        self.assertEqual(t.avgAge,0)
        #Team should be on allTeams pag
        response = self.client.get('/allTeams/25/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewAllTeams.html')
        self.assertContains(response,t.name)
        #Team views free agents
        response = self.client.get('/freeAgents/all/25/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewFreeAgents.html')
        #team offers contract to player
        #offer invalid contract salary
        response = self.client.post('/player/1/offerContract/',{'team':'1','salary':'20000001','length':'3','no_trade':'1','message':'Message Works'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Ensure this value is less than or equal to 20000000")
        #offer invalid length
        response = self.client.post('/player/1/offerContract/',{'team':'1','salary':'1000000','length':'20','no_trade':'False','message':'Message Works'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Ensure this value is less than or equal to 10.")
        #offer valid contract
        response = self.client.post('/player/1/offerContract/',{'team':'3','salary':'1000000','length':'2','no_trade':'True','message':'Message Works'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewTeam.html')

        #user should receive message notifying them of contract offer
        response = self.client.get('/users/2/viewMessages/received/10/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'userViewMessages.html')
        self.assertContains(response,"Team Team1 has offered TestPlayer1 a contract worth 1000000 per season for 2 season(s)" )
        
        #contract should appear on team's contract page
        response = self.client.get('/team/3/viewContracts/',follow=True)
        self.assertContains(response,"Offered")
        
        #Player rejects nonexistant contract
        response = self.client.post('/player/1/viewContracts/',{'Reject':'2'},follow=True)
        self.assertEqual(response.status_code,404)

        #Player accepts nonexistant contract
        response = self.client.post('/player/1/viewContracts/',{'Accept':'2'},follow=True)
        self.assertEqual(response.status_code,404)
        #Player accepts valid contract
        response = self.client.post('/player/1/viewContracts/',{'Accept':'1'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewPlayer.html')
        p = get_object_or_404(Player,pk = 1)
        self.assertEqual(p.team_id,3)
        self.assertEqual(p.salary,1000000)
        self.assertEqual(p.contract_end,2)
        self.assertEqual(p.free_agent,False)
        t = get_object_or_404(Team,pk=3)
        self.assertEqual(t.salary_used,1000000)
        self.assertEqual(t.salary_left,(2000000-1000000))
        self.assertEqual(t.numLWNeed,3)

        #user of should send  message notifying the team of accepted offer
        response = self.client.get('/users/2/viewMessages/received/10/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'userViewMessages.html')
        self.assertContains(response,"Player TestPlayer1 has accepted your contract offer of 1000000 for 2 season(s)!" )

        #team contract page should should contract accepted
        response = self.client.get('/team/3/viewContracts/',follow=True)
        self.assertContains(response,"Accepted")
        
        #Attempt to offer contract to non-Free agent player
        response = self.client.post('/player/1/offerContract/',{'team':'3','salary':'1000000','length':'2','no_trade':'True','message':'Message Works'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/offerPlayerContract.html')

        #message Players on Team
        title1="Message to Team"
        body1="Message Body to Team"
        response = self.client.post('/team/3/messagePlayersOnTeam/',{'title':title1,'body':body1},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewTeam.html')
        #check message correct
        m = get_object_or_404(Message,pk=3)
        self.assertEqual(m.sender_user_id,2)
        self.assertEquals(title1,m.title)
        self.assertEquals(body1,m.body)

        #user should receive message
        response = self.client.get('/users/2/viewMessages/received/10/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'userViewMessages.html')
        self.assertContains(response,"Message Body to Team" )

        
        #Team messages one player
        title2="Message to Player"
        body2="Team messages one player"
        response = self.client.post('/player/1/messagePlayer/',{'team_field':'3','title':title2,'body':body2},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewPlayer.html')
        m = get_object_or_404(Message,pk=4)
        self.assertEqual(m.sender_user_id,2)
        self.assertEquals(title2,m.title)
        self.assertEquals(body2,m.body)

        #user should receive message
        response = self.client.get('/users/2/viewMessages/received/10/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'userViewMessages.html')
        self.assertContains(response,"Team messages one player" )

        #No Team messages one player
        body2 = "No team messages one player"
        response = self.client.post('/player/1/messagePlayer/',{'team_field':'-1','title':title2,'body':body2},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewPlayer.html')
        m = get_object_or_404(Message,pk=5)
        self.assertEqual(m.sender_user_id,2)
        self.assertEquals(title2,m.title)
        self.assertEquals(body2,m.body)
        
        #user should receive message notifying them of contract offer
        response = self.client.get('/users/2/viewMessages/received/10/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'userViewMessages.html')
        self.assertContains(response,body2 )

    def test_view_free_agents_all_players(self):       
        response = self.client.post('/freeAgents/',follow=True)
        self.assertEqual(response.status_code,200)#redirects to /freeAgents/All/25/
        self.assertTemplateUsed(response,"hockey/viewFreeAgents.html")

        response = self.client.post('/freeAgents/All',follow=True)
        self.assertEqual(response.status_code,200)#redirects to /freeAgents/All/25/
        self.assertTemplateUsed(response,"hockey/viewFreeAgents.html")

        response = self.client.post('/freeAgents/All/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewFreeAgents.html")
        
        response = self.client.post('/freeAgents/L/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewFreeAgents.html")

        response = self.client.post('/freeAgents/C/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewFreeAgents.html")
        
        response = self.client.post('/freeAgents/R/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewFreeAgents.html")

        response = self.client.post('/freeAgents/D/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewFreeAgents.html")
        
        response = self.client.post('/freeAgents/G/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewFreeAgents.html")

        #Test viewing All Players
        response = self.client.post('/allPlayers/',follow=True)
        self.assertEqual(response.status_code,200)#redirects to /allPlayers/All/25/
        self.assertTemplateUsed(response,"hockey/viewAllPlayers.html")

        response = self.client.post('/allPlayers/All',follow=True)
        self.assertEqual(response.status_code,200)#redirects to /allPlayers/All/25/
        self.assertTemplateUsed(response,"hockey/viewAllPlayers.html")

        response = self.client.post('/allPlayers/All/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewAllPlayers.html")
        
        response = self.client.post('/allPlayers/L/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewAllPlayers.html")

        response = self.client.post('/allPlayers/C/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewAllPlayers.html")
        
        response = self.client.post('/allPlayers/R/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewAllPlayers.html")

        response = self.client.post('/allPlayers/D/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewAllPlayers.html")
        
        response = self.client.post('/allPlayers/G/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewAllPlayers.html")

        response = self.client.post('/allTeams/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewAllTeams.html")

        """response = self.client.post('/allUsers/25',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"hockey/viewAllUsers.html")
        """

class MessageTest(TestCase): 
    def setUp(self):
        self.client = Client()
        self.client.post('/accounts/register/',{'username':'UserTest2', 'email':'test@localhosttestregister.com','password1':'test','password2':'test'},follow=True)      
        self.client.post('/createTeam/',{'name':'TeamTest1','abbreviation':'TEA','arena_name':'Arena1'},follow=True)
        self.client.post('/accounts/register/',{'username':'UserTest2', 'email':'test@localhosttestregister2.com','password1':'test','password2':'test'},follow=True)  
        self.client.post('/creatingPlayer/',{'name':'PlayerTest1','position':'L','height':'70','weight':'180'},follow=True)
        self.client.post('/creatingPlayer/',{'name':'PlayerTest2','position':'R','height':'70','weight':'180'},follow=True)
        self.client.post('/createTeam/',{'name':'TeamTest2','abbreviation':'TEA','arena_name':'Arena1'},follow=True)
        
    
    def test_message(self):
        title = "Test Title"
        body = "Test Body"


class TeamTest(TestCase):
    def setup(self):
        self.client = Client()
        self.client.post('/accounts/register/',{'username':'teamTest1','password':'test'},follow=True)      

    def test_team_creation_creates_league(self):
        response = self.client.get('/index/')
        print response.content
