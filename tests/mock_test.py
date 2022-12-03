from mock.millionaire import runner


def main():
    test_select_correct_answers()
    test_guess_out_of_the_game()
    test_use_audience_help()
    test_use_halving_help()
    test_use_phone_help()
    test_random_scenario()


def test_select_correct_answers():
    runner.main(["Play", "Exit"], {
        "game_answers": ["OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"],
        "audience_answers": [], "halving_answers": [], "phone_answers": [], "out_of_game_answers": [],
        "return_prompt_answers": ["enter"]})


def test_guess_out_of_the_game():
    runner.main(["Play", "Exit"], {
        "game_answers": ["OK", "OK", "t", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"],
        "audience_answers": [], "halving_answers": [], "phone_answers": [], "out_of_game_answers": ["OK"],
        "return_prompt_answers": ["enter"]})


def test_use_halving_help():
    runner.main(["Play", "Exit"], {
        "game_answers": ["h", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"],
        "audience_answers": [], "halving_answers": ["h", "OK"], "phone_answers": [], "out_of_game_answers": [],
        "return_prompt_answers": ["enter"]})


def test_use_audience_help():
    runner.main(["Play", "Exit"], {
        "game_answers": ["OK", "h", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"],
        "audience_answers": [], "halving_answers": ["h", "OK"], "phone_answers": [], "out_of_game_answers": [],
        "return_prompt_answers": ["enter"]})


def test_use_phone_help():
    runner.main(["Play", "Exit"], {
        "game_answers": ["OK", "h", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK",
                         "OK"],
        "audience_answers": [], "halving_answers": [], "phone_answers": ["t", "m", "OK"], "out_of_game_answers": [],
        "return_prompt_answers": ["enter"]})


def test_random_scenario():
    runner.main(["Play", "Exit"], {"game_answers": ["a", "b", "c", "d"],
                             "audience_answers": [], "halving_answers": [], "phone_answers": [],
                             "out_of_game_answers": [], "return_prompt_answers": ["enter"]})


if __name__ == "__main__":
    main()
