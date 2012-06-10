from django.utils import unittest
from wuska.models import player
import datetime

class PlayerTestCase(unittest.TestCase):
    def testForward(self):
        self.assertEqual(5,"10")
        self.forward = player.objects.create(team_id = 1, user_id = 1, name="Test Player 1", age = 15, retired = false, height = 66, weight = 192, salary = 500000, contract_end = datetime.date(2009,4,2), no_trade = true, position = "F", style = "sniper", shooting = 88, passing = 85, stickHandling = 79, checking = 70, positioning = 70, endurance = 85, skating = 99, strength = 77, faceoff = 99, fighting = 49, awareness = 84)
        self.assertEqual(self.forward.name, "Test Player 1")
        self.assertEqual(self.forward.strength, 78)
