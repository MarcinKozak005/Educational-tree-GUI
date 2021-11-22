import tkinter as tk
import root as r
import list
import frame2 as f2
import redblacktree

frame = tk.Frame(r.frame)

for f in (frame, list.frame, f2.frame, redblacktree.frame):
    f.grid(row=0, column=0, sticky='nsew')

tk.Label(frame, text="Menu", bg='red').pack(fill='x')
tk.Button(frame, text='List', command=lambda: r.show_frame(list.frame)).pack()
tk.Button(frame, text='Frame 2', command=lambda: r.show_frame(f2.frame)).pack()
tk.Button(frame, text='Red-black tree', command=lambda: r.show_frame(redblacktree.frame)).pack()
