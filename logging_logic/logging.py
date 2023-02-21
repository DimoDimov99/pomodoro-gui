import os
import sys
from datetime import datetime
DELIMITER = "------------------"
ROOT_PATH = os.getcwd()


def return_to_root_dir():
    try:
        os.chdir(ROOT_PATH)
        print(f"Returned to {ROOT_PATH}")
    except OSError as error:
        print(error)
        sys.exit(1)


def create_folder():
    foldername = "POMODORO_LOGS"
    destination = os.path.join(ROOT_PATH, foldername)
    try:
        os.mkdir(destination)
    except FileExistsError:
        os.chdir(destination)
    except OSError as error:
        print(error)
        sys.exit(1)
    try:
        os.chdir(destination)
    except OSError as error:
        print(error)
        sys.exit(1)
    print(f"Current dir: {os.getcwd()}")


def log_pomodoro_session(message):
    create_folder()
    dt = datetime.now()
    filename = dt.strftime("%A_pomodoro.txt")
    with open(filename, "a", encoding="utf8") as file:
        file.write(f"{message}\n")
        file.write(
            f"[{datetime.now().strftime('%B %d %Y')}] at [{datetime.now().strftime('%H:%M:%S')}]\n")
        file.write(DELIMITER)
        file.write("\n")
    return_to_root_dir()
