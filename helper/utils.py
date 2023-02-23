COMMANDS = {
    "usage": "python3 main.py",
    "optional arguments": "WORK_SESSION=(int) SHORT_BREAK=(int) LONG_BREAK=(int)",
    "example run no arguments": "python3 main.py",
    "example run with arguments": "python3 main.py 25(pomodoro work session) 5(short break) 15 (long break)",
}


def display_help():
    for key, value in COMMANDS.items():
        print(f"{key}: {value}")
