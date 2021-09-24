# https://youtu.be/YXPyB4XeYLA?t=1201

import tkinter as tk

root = tk.Tk()

def myClick():
    l = tk.Label(root, text="I appeared!")
    l.pack()

b = tk.Button(root, text="Click me", padx=20,command=myClick)
b.pack()


root.mainloop()