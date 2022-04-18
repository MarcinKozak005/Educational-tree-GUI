# Root (Main window) frame file. Contains miscellaneous functions and classes

from enum import Enum

import customtkinter as ctk

from core.constants import animation_unit


def show_frame(f):
    f.tkraise()


def wait(time):
    if time <= animation_unit:
        frame.update()
        frame.after(time)
    else:
        counter = time / animation_unit
        while counter > 0:
            frame.update()
            frame.after(animation_unit)
            counter -= 1


class Action(Enum):
    insert = 1
    delete = 2
    search = 3
    min = 4
    max = 5
    mean = 6
    median = 7


class Mode(Enum):
    value = 1
    node = 2
    down = 3
    up = 4


frame = ctk.CTk()
frame.title('Educational tree GUI')
frame.state('zoomed')
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
