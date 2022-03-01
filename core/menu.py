import tkinter as tk

import btree.main as bt
import core.root as r
import rbt.main as rbt

frame = tk.Frame(r.frame)

for f in (frame, rbt.frame, bt.frame):
    f.grid(row=0, column=0, sticky='nsew')

tk.Label(frame, text='Menu', bg='red').pack(fill='x')
tk.Button(frame, text='Red-black tree', command=lambda: r.show_frame(rbt.frame)).pack()
tk.Button(frame, text='B-tree', command=lambda: r.show_frame(bt.frame)).pack()
