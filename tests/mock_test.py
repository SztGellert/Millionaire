import os, sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/millionaire')
from mock.millionaire import runner


def main():
    use_halving_help()
    use_audience_help()
    use_phone_help()
    select_correct_answers()


def select_correct_answers():
    runner.main(["p", "e"], {
        "game_answers": ["OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"],
        "help_answers": []})


def use_halving_help():
    runner.main(["p", "e"], {
        "game_answers": ["OK", "h", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"],
        "help_answers": ["h", "OK"]})


def use_audience_help():
    runner.main(["p", "e"], {
        "game_answers": ["OK", "h", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"],
        "help_answers": ["h", "OK"]})


def use_phone_help():
    runner.main(["p", "e"], {
        "game_answers": ["OK", "h", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK",
                         "OK"],
        "help_answers": ["h", "m", "OK"]})


def mock_test_scenario_one():
    runner.main(["p", "e"], {"game_answers": ["a", "b", "c", "d"], "help_answers": []})


if __name__ == "__main__":
    main()
