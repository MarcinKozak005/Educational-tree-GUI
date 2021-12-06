import tkinter as tk
import core.root as r
import core.menu as m

frame = tk.Frame(r.frame)
tk.Label(frame, text="Frame2", bg='yellow').pack(fill='x')
tk.Button(frame, text='Back', command=lambda: r.show_frame(m.frame)).pack()
