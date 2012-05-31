"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from datetime import datetime
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from wuska.hockey.models import Player, Team, League, Arena
class PlayerTest(TestCase):
    
    def setUp(self):
        team_id = 1
        user_id = 1
        name = "TestUser1"
        upgrades = 1
        level = 1
        experience = 2
        age = 20
        retired = False
        height = 60
        weight = 160
        salary = 600000
        contract_end = 0
        no_trade = False
        position = "D"
        style = 0
        shooting = 100
        passing = 100
        stickHandling = 100
        checking = 100
        positioning = 100
        endurance = 100
        skating = 100
        strength = 100
        faceoff = 100
        fighting = 100
        awareness = 100
        leadership = 100
        helmet = 1
        gloves = 1
        shoulder_pads = 1
        pants = 1
        skates = 1
        stick = 1
        free_agent = True
        self.player = Player.objects.create(team_id = team_id, user_id = user_id, upgrades = upgrades, level = level, experience = experience, name = name, age = age, retired = retired, height = height, weight = weight, salary =salary, contract_end = contract_end, no_trade = no_trade, position = position, style = style, shooting = shooting, passing = passing, stickHandling = stickHandling, checking = checking, positioning = positioning, endurance = endurance, skating = skating, strength = strength, faceoff = faceoff, fighting = fighting, awareness = awareness, leadership = leadership, helmet = helmet, gloves = gloves, shoulder_pads = shoulder_pads, pants = pants, skates = skates, stick = stick, free_agent = free_agent)

    def test_player(self):
        self.assertEqual(self.player.skates, 100)
        self.assertEqual(self.player.name, "hello")

class PlayerTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_cant_login_via_login_page(self):
        self.browser.get(self.live_server_url + '/accounts/login/')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        self.assertIn('',username_box.text)
        self.assertIn('',password_box.text)
        self.browser.find_element_by_id('submit').click()
        self.assertIn('/accounts/login', self.browser.current_url)
        
    def test_can_register_new_user(self):
        self.browser.get(self.live_server_url + '/accounts/register/')
        username_box = self.browser.find_element_by_id('id_username')
        email_box = self.browser.find_element_by_id('id_email')
        password1_box = self.browser.find_element_by_id('id_password1')
        password2_box = self.browser.find_element_by_id('id_password2')
        self.assertIn('',username_box.text)
        self.assertIn('',email_box.text)
        self.assertIn('',password1_box.text)
        self.assertIn('',password2_box.text)
        self.browser.find_element_by_id('submit').click()
        self.assertIn('/accounts/register', self.browser.current_url)

        self.browser.get(self.live_server_url + '/accounts/register/')
        username_box = self.browser.find_element_by_id('id_username').send_keys('Test')
        email_box = self.browser.find_element_by_id('id_email')
        email_box.send_keys('testuser@localhostadfsdfsf')
        self.browser.find_element_by_id('submit').click()
        self.assertIn('/accounts/register', self.browser.current_url)
        email_box = self.browser.find_element_by_id('id_email')
        email_box.send_keys('.com')
        password1_box = self.browser.find_element_by_id('id_password1')
        password1_box.send_keys('testing1')
        password2_box = self.browser.find_element_by_id('id_password2')
        password2_box.send_keys('ExFail')
        self.browser.find_element_by_id('submit').click()
        self.assertIn('/accounts/register', self.browser.current_url)
        
        
        
        
