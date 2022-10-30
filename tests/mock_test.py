import os, sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/millionaire')
from mock.millionaire import runner


def main():
    select_correct_answers()


def select_correct_answers():
    runner.main(["p"], ["OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"])


def mock_test_scenario_one():
    runner.main(["p"], ["a", "b", "c", "d"])


if __name__ == "__main__":
    main()
b