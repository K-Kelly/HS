from django.shortcuts import get_object_or_404
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from wuska.hockey.models import *
from django.test.client import Client

class leagueTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/accounts/register/',{'username':'PlayerTest1', 'email':'test@localhosttestregister.com','password1':'test','password2':'test'},follow=True) 

    def test_schedule_games(self):
        i = 1
        while (i<31):                      
            response = self.client.post('/createTeam/',{'name':'Team%s'%(i),'abbreviation':'TEA','arena_name':'Arena1'},follow=True)
            self.assertEqual(response.status_code,200)
            t = get_object_or_404(Team,name="Team%s"%(i))
            self.assertEqual(t.name, 'Team%s'%(i))
            self.assertEqual(t.league_id,1)
            i+=1
        response = self.client.post('/createTeam/',{'name':'Team%s'%(i),'abbreviation':'TEA','arena_name':'Arena1'},follow=True)
        self.assertEqual(response.status_code,200)
        t = get_object_or_404(Team,name="Team%s"%(i))
        self.assertEqual(t.name, 'Team%s'%(i))
        self.assertEqual(t.league_id,2)

        response = self.client.get('/adminActions/scheduleNewSeason/')
        self.assertTemplateUsed(response,'404.html')
