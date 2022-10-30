import os, sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/millionaire')
from mock.millionaire import runner


def main():
    use_help()


def select_correct_answers():
    runner.main(["p"], ["OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"])


def use_help():
    runner.main(["p"], ["OK", "h", "h", "OK"])


def mock_test_scenario_one():
    runner.main(["p"], ["a", "b", "c", "d"])


if __name__ == "__main__":
    main()
