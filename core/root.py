import tkinter as tk


def show_frame(f):
    f.tkraise()


def wait(time):
    frame.update()
    frame.after(time)


frame = tk.Tk()
frame.state('zoomed')
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
