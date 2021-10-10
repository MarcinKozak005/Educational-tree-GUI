import tkinter as tk
import root as r
import menu as m

frame = tk.Frame(r.frame)
tk.Label(frame,text="Frame1",bg='green').pack(fill='x')
tk.Button(frame,text='Back',command=lambda: r.show_frame(m.frame)).pack()
