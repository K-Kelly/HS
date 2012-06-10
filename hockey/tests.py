"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.shortcuts import get_object_or_404
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from wuska.hockey.models import *
from django.test.client import Client

class PlayerTest(TestCase): 
    def setUp(self):
        self.client = Client()
        self.client.post('/accounts/register/',{'username':'PlayerTest1', 'email':'test@localhosttestregister.com','password1':'test','password2':'test'},follow=True)
    def test_create_Player(self):
        #Create Player
        response = self.client.post('/creatingPlayer/',{'name':'TestPlayer1','position':'L','height':'70','weight':'180'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewPlayer.html')
        p = get_object_or_404(Player,pk = 1)
        #Compare created player to itself after being retrieved
        self.assertEqual(p.name, "TestPlayer1")
        self.assertEqual(p.team_id, -1)
        self.assertEqual(p.user_id, 1)
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
        t = get_object_or_404(Team,pk=1)
        self.assertEqual(t.name, 'Team1')
        self.assertEqual(t.owner, 1)
        self.assertEqual(t.general_Manager,-1)
        self.assertEqual(t.league_id,-1)
        self.assertEqual(t.arena.name,'Arena1')
        self.assertEqual(t.funds,2000000)
        self.assertEqual(t.salary_used,0)
        self.assertEqual(t.salary_left,2000000)
        #Team views free agents
        response = self.client.get('/freeAgents/all/')
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
        response = self.client.post('/player/1/offerContract/',{'team':'1','salary':'1000000','length':'2','no_trade':'True','message':'Message Works'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewTeam.html')
        
        #Player rejects invalid contract
        response = self.client.post('/player/1/viewContracts/',{'Reject':'2'},follow=True)
        self.assertEqual(response.status_code,404)
        #Player accepts invalid contract
        response = self.client.post('/player/1/viewContracts/',{'Accept':'2'},follow=True)
        self.assertEqual(response.status_code,404)
        #Player accepts valid contract
        response = self.client.post('/player/1/viewContracts/',{'Accept':'1'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewPlayer.html')
        p = get_object_or_404(Player,pk = 1)
        self.assertEqual(p.team_id,1)
        self.assertEqual(p.salary,1000000)
        self.assertEqual(p.contract_end,2)
        self.assertEqual(p.free_agent,False)
        t = get_object_or_404(Team,pk=1)
        self.assertEqual(t.salary_used,1000000)
        self.assertEqual(t.salary_left,(2000000-1000000))
        

        #message Players on Team
        title1="Message to Team"
        body1="Message Body to Team"
        response = self.client.post('/team/1/messageTeam',{'title':title1,'body':body1},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewTeam.html')
        #check message correct
        m = get_object_or_404(Message,pk=1)
        self.assertEqual(m.sender_user_id,1)
        self.assertEquals(title1,m.title)
        self.assertEquals(body1,m.body)
        p = get_object_or_404(Player,pk = 1)
        p1_message = p.messages.all()[0]
        self.assertEquals(p1_message,m)
        
        #Team messages one player
        title2="Message to Player"
        body2="Message Body to Player"
        response = self.client.post('/player/1/messagePlayer/',{'team_field':'1','title':title2,'body':body2},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewPlayer.html')
        m = get_object_or_404(Message,pk=2)
        self.assertEqual(m.sender_user_id,1)
        self.assertEquals(title2,m.title)
        self.assertEquals(body2,m.body)
        p = get_object_or_404(Player,pk = 1)
        p1_message = p.messages.all()[1]
        self.assertEquals(p1_message,m)

        #No Team messages one player
        response = self.client.post('/player/1/messagePlayer/',{'team_field':'-1','title':title2,'body':body2},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/viewPlayer.html')
        m = get_object_or_404(Message,pk=3)
        self.assertEqual(m.sender_user_id,1)
        self.assertEquals(title2,m.title)
        self.assertEquals(body2,m.body)
        p = get_object_or_404(Player,pk = 1)
        p1_message = p.messages.all()[2]
        self.assertEquals(p1_message,m)

        #player views messages
        response = self.client.get('/player/1/viewMessages/10/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'hockey/playerViewMessages.html')
        self.assertContains(response,title1)
        self.assertContains(response,body1)
        self.assertContains(response,title2)
        self.assertContains(response,body2,count=2)
        
"""    
    def test_messaging(self):
        title = "Test Message Title"
        body = "Test Message Body"
        message = Message(sender_user_id=self.player1.user_id,sender_player_id=self.player1.id,sender_team_id=-1,receiver_team_id=-1,title=title,body=body)
        message.save()
        message.receiver_players.add(self.player2)
        message.save()
        self.player1.messages.add(message)
        self.player1.save()
        self.player2.messages.add(message)
        m_id = message.id
        p1_message = self.player1.messages.all().filter(id = m_id)
        self.assertEquals(message,p1_message)
        self.assertEquals(title,p1_message.title)
        self.assertEquals(body,p1_message.body)
        self.assertEquals(self.player1.user_id,p1_message.sender_user_id)
        self.assertEquals(self.player1.id,p1_message.sender_player_id)
        self.assertEquals(-1,p1_message.sender_team_id)
        self.assertEquals(-1,p1_message.receiver_team_id)
        p2_message = self.player2.messages.all().filter(id = m_id)
        self.assertEquals(message,p2_message)
        self.assertEquals(title,p2_message.title)
        self.assertEquals(body,p2_message.body)
        self.assertEquals(self.player1.user_id,p2_message.sender_user_id)
        self.assertEquals(self.player1.id,p2_message.sender_player_id)
        self.assertEquals(-1,p2_message.sender_team_id)
        self.assertEquals(-1,p2_message.receiver_team_id)
"""        


"""def setUp(self):
        upgrades = 10
        level = 1
        experience = 2
        age = 20
        retired = False
        height = 60
        weight = 160
        salary = 600000
        contract_end = 0
        no_trade = False
        style = 0
        shooting = 50
        passing = 51
        stickHandling = 52
        checking = 53
        positioning = 54
        endurance = 55
        skating = 56
        strength = 57
        faceoff = 58
        fighting = 59
        awareness = 60
        leadership = 61
        helmet = 1
        gloves = 1
        shoulder_pads = 1
        pants = 1
        skates = 1
        stick = 1
        free_agent = True
        self.player1 = Player.objects.create(team_id = -1, user_id = 1, upgrades = upgrades, level = level, experience = experience, name = "TestPlayer1", age = age, retired = retired, height = height, weight = weight, salary =salary, contract_end = contract_end, no_trade = no_trade, position = "D", style = style, shooting = shooting, passing = passing, stickHandling = stickHandling, checking = checking, positioning = positioning, endurance = endurance, skating = skating, strength = strength, faceoff = faceoff, fighting = fighting, awareness = awareness, leadership = leadership, helmet = helmet, gloves = gloves, shoulder_pads = shoulder_pads, pants = pants, skates = skates, stick = stick, free_agent = free_agent)
        self.player1.save()
"""
