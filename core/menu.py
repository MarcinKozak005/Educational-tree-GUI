import tkinter as tk
import core.root as r
import drafts.list as li
import drafts.frame2 as f2
import redblack_tree.main as rbt
import btree.main as bt

frame = tk.Frame(r.frame)

for f in (frame, li.frame, f2.frame, rbt.frame, bt.frame):
    f.grid(row=0, column=0, sticky='nsew')

tk.Label(frame, text="Menu", bg='red').pack(fill='x')
tk.Button(frame, text='List', command=lambda: r.show_frame(li.frame)).pack()
tk.Button(frame, text='Frame 2', command=lambda: r.show_frame(f2.frame)).pack()
tk.Button(frame, text='Red-black tree', command=lambda: r.show_frame(rbt.frame)).pack()
tk.Button(frame, text='B-tree', command=lambda: r.show_frame(bt.frame)).pack()
