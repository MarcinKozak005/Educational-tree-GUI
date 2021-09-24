# https://youtu.be/YXPyB4XeYLA?t=641

import tkinter as tk

root = tk.Tk()

label1 = tk.Label(root, text="Test1")
label2 = tk.Label(root, text="Test2")

label1.grid(row=0,column=1)
label2.grid(row=1,column=1)


root.mainloop()