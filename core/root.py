import tkinter as tk


def show_frame(f):
    f.tkraise()


frame = tk.Tk()
frame.state('zoomed')
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
