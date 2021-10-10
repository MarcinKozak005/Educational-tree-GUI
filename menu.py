import tkinter as tk
import root as r
import frame1 as f1
import frame2 as f2

frame = tk.Frame(r.frame)

for f in (frame,f1.frame, f2.frame):
    f.grid(row=0, column=0, sticky='nsew')

tk.Label(frame, text="Menu",bg='red').pack(fill='x')
tk.Button(frame,text='Frame 1',command=lambda: r.show_frame(f1.frame)).pack()
tk.Button(frame,text='Frame 2',command=lambda: r.show_frame(f2.frame)).pack()