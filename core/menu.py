import tkinter as tk

import core.root as r
import bt.main as bt
import rbt.main as rbt
import avlt.main as avlt
import bpt.main as bpt

frame = tk.Frame(r.frame)

for f in (frame, rbt.frame, bt.frame, avlt.frame, bpt.frame):
    f.grid(row=0, column=0, sticky='nsew')

tk.Label(frame, text='Menu', bg='red').pack(fill='x')
tk.Button(frame, text='Red-black tree', command=lambda: r.show_frame(rbt.frame)).pack()
tk.Button(frame, text='B-tree', command=lambda: r.show_frame(bt.frame)).pack()
tk.Button(frame, text='AVL Tree', command=lambda: r.show_frame(avlt.frame)).pack()
tk.Button(frame, text='B+tree', command=lambda: r.show_frame(bpt.frame)).pack()
