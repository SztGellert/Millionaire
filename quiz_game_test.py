import unittest

import millionaire.quiz_game as quiz
import json


class TestSum(unittest.TestCase):

    def test_halving(self):
        halved_answers = quiz.calculate_halved_answers({"a": "30", "b": "60", "c": "300", "d": "1"}, "60")
        self.assertIn("60", halved_answers.values())
        self.assertTrue(list(halved_answers.values()).count("") == 2)

    def test_audience_chances(self):
        chances = quiz.get_chances({"a": "300", "b": "1", "c": "30", "d": "60"}, "60")
        result = sum(chances)
        self.assertEqual(100, result)

    """"
    This test can not fit to unit tests but can display how audience's help works.
    def test_audience_help(self):
        pygame.init()
        chances = quiz_game.audience_help("How many seconds are in a minute?", {"a": "300", "b": "1", "c": "30", "d": "60"}, "60")
    """

    def test_update_settings_file(self):
        quiz.write_content_to_file("settings.json", {})
        settings = [
            {"lang": "en", "topic": "All"},
            {"lang": "en", "topic": "Phisycs"},
            {"lang": "hu", "topic": "Fizika"},
            {"lang": "en", "topic": "Phisycs"}
        ]
        for i in settings:
            with open("settings.json", "r", encoding="UTF-8") as file:
                json.dump(settings, file)
            file_data = json.load(file)
            self.assertEqual(file_data, i)


if __name__ == "__main__":
    unittest.main()
