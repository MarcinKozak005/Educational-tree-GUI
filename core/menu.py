# Menu frame file

import customtkinter as ctk

import asa_graph.main as asag
import avbpt.main as avbpt
import avbt.main as avbt
import avlt.main as avlt
import bpt.main as bpt
import bt.main as bt
import core.root as r
import rbt.main as rbt
import structures_comparison.main as comp
from core.constants import light_green

frame = ctk.CTkFrame(r.frame)
for f in (frame, rbt.frame, avlt.frame, bt.frame, bpt.frame, avbt.frame, avbpt.frame, asag.frame, comp.frame):
    f.grid(row=0, column=0, sticky='nsew')

ctk.CTkLabel(frame, text='Menu', bg=light_green, text_font=20).pack(fill='x', pady=(15, 15))
buttons_arguments = {'width': 50, 'height': 20}
ctk.CTkButton(frame, text='Red-black tree', command=lambda: r.show_frame(rbt.frame)).pack(pady=(5, 5))
ctk.CTkButton(frame, text='AVL Tree', command=lambda: r.show_frame(avlt.frame)).pack(pady=(5, 5))
ctk.CTkButton(frame, text='B-tree', command=lambda: r.show_frame(bt.frame)).pack(pady=(5, 5))
ctk.CTkButton(frame, text='B+tree', command=lambda: r.show_frame(bpt.frame)).pack(pady=(5, 5))
ctk.CTkButton(frame, text='AVB-tree', command=lambda: r.show_frame(avbt.frame)).pack(pady=(5, 5))
ctk.CTkButton(frame, text='AVB+tree', command=lambda: r.show_frame(avbpt.frame)).pack(pady=(5, 5))
ctk.CTkButton(frame, text='ASA-Graph', command=lambda: r.show_frame(asag.frame)).pack(pady=(5, 5))
ctk.CTkButton(frame, text='Comparison', command=lambda: r.show_frame(comp.frame)).pack(pady=(5, 5))
