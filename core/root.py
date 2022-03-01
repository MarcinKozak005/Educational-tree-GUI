import tkinter as tk
from enum import Enum


def show_frame(f):
    f.tkraise()


def wait(time):
    frame.update()
    frame.after(time)


hint_frame = 'hint_frame'
grey_node = 'grey_node'
exp_txt = 'exp_txt'


class Action(Enum):
    insert = 1
    delete = 2
    search = 3


frame = tk.Tk()
frame.state('zoomed')
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
