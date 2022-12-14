# pylint: skip-file

def return_user_input_windows() -> bytes:
    import msvcrt

    return msvcrt.getch()

def return_user_input_linux() -> str:
    from curtsies import Input
    with Input() as input_generator:
        for c in input_generator:

            return c