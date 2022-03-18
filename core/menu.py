# Menu frame file

import tkinter as tk

import avlt.main as avlt
import bpt.main as bpt
import bt.main as bt
import core.root as r
import rbt.main as rbt
import avbt.main as avbt
import avbpt.main as avbpt

frame = tk.Frame(r.frame)
for f in (frame, rbt.frame, bt.frame, avlt.frame, bpt.frame, avbt.frame, avbpt.frame):
    f.grid(row=0, column=0, sticky='nsew')

tk.Label(frame, text='Menu', bg='red').pack(fill='x')
tk.Button(frame, text='Red-black tree', command=lambda: r.show_frame(rbt.frame)).pack()
tk.Button(frame, text='B-tree', command=lambda: r.show_frame(bt.frame)).pack()
tk.Button(frame, text='AVL Tree', command=lambda: r.show_frame(avlt.frame)).pack()
tk.Button(frame, text='B+tree', command=lambda: r.show_frame(bpt.frame)).pack()
tk.Button(frame, text='AVB-tree', command=lambda: r.show_frame(avbt.frame)).pack()
tk.Button(frame, text='AVB+tree', command=lambda: r.show_frame(avbpt.frame)).pack()

