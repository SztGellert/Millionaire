import unittest

from millionaire.quiz_game import game


class TestSum(unittest.TestCase):
    def test_create_chances(self):
        chances_list = game.get_chances()
        result = sum(chances_list)
        self.assertEqual(100, result)


if __name__ == "__main__":
    unittest.main()
