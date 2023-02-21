import os
import sys
import tkinter
from tkinter import *
import tkinter.messagebox
import math
from time import strftime
from datetime import datetime
from logging_logic import logging

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 0.001
SHORT_BREAK_MIN = 0.001
LONG_BREAK_MIN = 0.001
reps = 0
pomodoro_reps = 1
timer = ""


# ---------------------------- Buttons fix ------------------------------- #
def start_button_clicked():
    start_button.config(state="disabled")
    reset_button.config(state="normal")


def reset_button_clicked():
    start_button.config(state="normal")
    reset_button.config(state="disabled")


# ---------------------------- Popup ------------------------------- #
def start_working():
    tkinter.messagebox.showinfo(title="Work", message="Start Working!")


def short_break():
    tkinter.messagebox.showinfo(title="Break", message="Short Break!")


def long_break():
    tkinter.messagebox.showinfo(title="Break", message="Long Break!")


# ---------------------------- CONSTANTS ------------------------------- #
def focus_window(option):
    if option == "on":
        window.deiconify()
        window.focus_force()
        window.attributes("-topmost", True)
    elif option == "off":
        window.attributes("-topmost", False)


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    reset_button_clicked()
    global pomodoro_reps
    global reps
    window.after_cancel(timer)
    pomodoro_reps = 1
    reps = 0
    canvas.itemconfig(timer_text, text="START")
    timer_label.config(text="Timer")
    checkmarks.config(text="")
    start_button.config(state="normal")
    reset_button.config(state="disabled")

# ---------------------------- LOG RESET ------------------------------- #


def log_reset():

    ROOT_PATH = os.getcwd()
    try:
        dt = datetime.now()
        current_day = dt.strftime("%A")
        file_name = dt.strftime("%A_pomodoro.txt")
        os.chdir("POMODORO_LOGS")
        os.remove(file_name)
        print(f"Pomodoro file for {current_day} is removed")
        os.chdir(ROOT_PATH)
    except OSError as errror:
        print(errror)
        sys.exit(1)

# ---------------------------- DISPLAY TIME ------------------------------- #


def time():
    string = strftime('%H:%M:%S %p')
    lbl.config(text=string)
    lbl.after(1000, time)

# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    start_button_clicked()
    global reps
    global pomodoro_reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        logging.log_pomodoro_session(
            f"POMODORO SESSION [{pomodoro_reps}] COMPLETED (LONG BREAK)")
        pomodoro_reps += 1
        focus_window("on")
        window.bell()
        # long_break()
        count_down(long_break_sec)
        timer_label.config(text="Break", bg=YELLOW,
                           font=(FONT_NAME, 50), foreground=RED)
    elif reps % 2 == 0:
        logging.log_pomodoro_session(
            f"POMODORO SESSION [{pomodoro_reps}] COMPLETED (SHORT BREAK)")
        pomodoro_reps += 1
        focus_window("on")
        window.bell()
        # short_break()
        count_down(short_break_sec)
        timer_label.config(text="Break", bg=YELLOW,
                           font=(FONT_NAME, 50), foreground=PINK)
    else:
        logging.log_pomodoro_session(
            f"POMODORO WORK SESSIONS [{pomodoro_reps}] STARTED ({WORK_MIN})")
        focus_window("off")
        window.bell()
        # start_working()
        count_down(work_sec)
        timer_label.config(text="Work", bg=YELLOW, font=(
            FONT_NAME, 50), foreground=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        marks = 0
        work_sessions = math.floor(reps / 2)
        marks = work_sessions
        # for _ in range(work_sessions):
        # marks += "✔"
        # pass
        checkmarks.config(text=marks, bg=YELLOW, font=(
            FONT_NAME, 23, "bold"), foreground=GREEN)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
window.iconphoto(False, tkinter.PhotoImage("images/icon.png"))
window.config(padx=100, pady=50, bg=YELLOW)


timer_label = Label(text="Timer", bg=YELLOW, font=(
    FONT_NAME, 50), foreground=GREEN)
timer_label.grid(column=1, row=0)

start_button = Button(text="Start", bg=YELLOW,
                      highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", bg=YELLOW,
                      highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)
reset_button.config(state="disabled")

checkmarks = Label(text="", bg=YELLOW, font=(
    FONT_NAME, 23, "bold"), foreground=GREEN)
checkmarks.grid(column=1, row=5)

canvas = Canvas(width=200, height=240, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="images/tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(
    100, 150, text="START", fill="#fff", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

test_button = Button(text="Reset LOG", bg=YELLOW,
                     highlightthickness=0, command=log_reset)
test_button.grid(column=1, row=2)

lbl = Label(window, font=("calibri", 20, "bold"), bg=YELLOW)
lbl.grid(column=1, row=6)
time()

window.resizable(width=False, height=False)

window.mainloop()
