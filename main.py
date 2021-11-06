import tkinter
from tkinter import *
import tkinter.messagebox
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
reps = 0
timer = None


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
    global reps
    window.after_cancel(timer)
    reps = 0
    canvas.itemconfig(timer_text, text="START")
    timer_label.config(text="Timer")
    checkmarks.config(text="")
    start_button.config(state="normal")
    reset_button.config(state="disabled")


# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    start_button_clicked()
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        focus_window("on")
        window.bell()
        # long_break()
        count_down(long_break_sec)
        timer_label.config(text="Break", bg=YELLOW, font=(FONT_NAME, 50), foreground=RED)
    elif reps % 2 == 0:
        focus_window("on")
        window.bell()
        # short_break()
        count_down(short_break_sec)
        timer_label.config(text="Break", bg=YELLOW, font=(FONT_NAME, 50), foreground=PINK)
    else:
        focus_window("off")
        window.bell()
        # start_working()
        count_down(work_sec)
        timer_label.config(text="Work", bg=YELLOW, font=(FONT_NAME, 50), foreground=GREEN)


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
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        checkmarks.config(text=marks, bg=YELLOW, font=(FONT_NAME, 23, "bold"), foreground=GREEN)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
window.iconphoto(False, tkinter.PhotoImage("icon.png"))
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = Label(text="Timer", bg=YELLOW, font=(FONT_NAME, 50), foreground=GREEN)
timer_label.grid(column=1, row=0)

start_button = Button(text="Start", bg=YELLOW, highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", bg=YELLOW, highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)
reset_button.config(state="disabled")

checkmarks = Label(text="", bg=YELLOW, font=(FONT_NAME, 23, "bold"), foreground=GREEN)
checkmarks.grid(column=1, row=3)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="START", fill="#fff", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

window.resizable(width=False, height=False)
window.mainloop()
