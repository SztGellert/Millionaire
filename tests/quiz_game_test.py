import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../millionaire')
from millionaire.quiz_game import quiz_game


class TestSum(unittest.TestCase):

    def test_halving(self):
        halved_answers = quiz_game.calculate_halved_answers({"a": "30", "b": "60", "c": "300", "d": "1"}, "60")
        self.assertIn("60", halved_answers.values())
        self.assertTrue(list(halved_answers.values()).count("") == 2)

    def test_audience_chances(self):
        chances = quiz_game.get_chances({"a": "300", "b": "1", "c": "30", "d": "60"}, "60")
        result = sum(chances)
        self.assertEqual(100, result)



if __name__ == "__main__":
    unittest.main()
