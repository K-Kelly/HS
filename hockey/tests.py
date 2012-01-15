"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from datetime import datetime
from django.test import TestCase
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
        self.player = Player.objects.create(team_id = team_id, user_id = user_id, upgrades = upgrades, level = level, experience = experience, name = name, age = age, retired = retired, height = height, weight = weight, salary =salary, contract_end = contract_end, no_trade = no_trade, position = position, style = style, shooting = shooting, passing = passing, stickHandling = stickHandling, checking = checking, positioning = positioning, endurance = endurance, skating = skating, strength = strength, faceoff = faceoff, fighting = fighting, awareness = awareness, leadership = leadership, helmet = helmet, gloves = gloves, shoulder_pads = shoulder_pads, pants = pants, skates = skates, stick = stick)

    def test_player(self):
        self.assertEqual(self.player.skates, 100)
        self.assertEqual(self.player.name, "hello")
