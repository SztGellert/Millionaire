import os
import sys
import unittest
import pygame.mixer

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../millionaire')
from millionaire.quiz_game import quiz_game

class TestSum(unittest.TestCase):

    def test_create_chances(self):
        chances_list = quiz_game.get_chances()
        result = sum(chances_list)
        self.assertEqual(100, result)

    def test_halving(self):
        pygame.mixer.init()
        quiz_game.halving("How many seconds are in a minute?", {"a": "60", "b": "30", "c": "1", "d": "300"}, "60")

    def test_audience(self):
        pygame.mixer.init()
        quiz_game.audience_help("How many seconds are in a minute?", {"a": "300", "b": "1", "c": "30", "d": "60"}, "60")


if __name__ == "__main__":
    unittest.main()
