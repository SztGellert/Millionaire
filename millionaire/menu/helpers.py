# pylint: skip-file

def return_user_input_windows() -> bytes:
    import msvcrt
    user_input = msvcrt.getch()
    return user_input

def return_user_input_linux() -> bytes:
    import getch
    user_input = getch.getch()
    return user_input