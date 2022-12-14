import unittest

from millionaire.quiz_game import quiz_game


class TestSum(unittest.TestCase):

    def test_halving(self):
        halved_answers = quiz_game.calculate_halved_answers({"a": "30", "b": "60", "c": "300", "d": "1"}, "60")
        self.assertIn("60", halved_answers.values())
        self.assertTrue(list(halved_answers.values()).count("") == 2)

    def test_audience_chances(self):
        chances = quiz_game.get_chances({"a": "300", "b": "1", "c": "30", "d": "60"}, "60")
        result = sum(chances.values())
        self.assertEqual(100, result)

    """"
    This test can not fit to unit tests but can display how audience's help works.
    def test_audience_help(self):
        pygame.init()
        chances = quiz_game.audience_help("How many seconds are in a minute?", {"a": "300", "b": "1", "c": "30", "d": "60"}, "60")
    """


if __name__ == "__main__":
    unittest.main()
