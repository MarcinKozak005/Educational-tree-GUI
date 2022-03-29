# Menu frame file

import tkinter as tk

import avbpt.main as avbpt
import avbt.main as avbt
import avlt.main as avlt
import bpt.main as bpt
import bt.main as bt
import core.root as r
import rbt.main as rbt
from core.constants import light_green

frame = tk.Frame(r.frame)
for f in (frame, rbt.frame, avlt.frame, bt.frame, bpt.frame, avbt.frame, avbpt.frame):
    f.grid(row=0, column=0, sticky='nsew')

tk.Label(frame, text='Menu', bg=light_green).pack(fill='x')
tk.Button(frame, width=15, height=2, text='Red-black tree', command=lambda: r.show_frame(rbt.frame)).pack()
tk.Button(frame, width=15, height=2, text='AVL Tree', command=lambda: r.show_frame(avlt.frame)).pack()
tk.Button(frame, width=15, height=2, text='B-tree', command=lambda: r.show_frame(bt.frame)).pack()
tk.Button(frame, width=15, height=2, text='B+tree', command=lambda: r.show_frame(bpt.frame)).pack()
tk.Button(frame, width=15, height=2, text='AVB-tree', command=lambda: r.show_frame(avbt.frame)).pack()
tk.Button(frame, width=15, height=2, text='AVB+tree', command=lambda: r.show_frame(avbpt.frame)).pack()
