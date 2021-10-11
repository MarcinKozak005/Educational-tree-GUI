import tkinter as tk
from tkinter import font
import root as r
import menu as m

position = (100,100)
node_size = 26
half_node_size = node_size/2

def draw_node(text,canvas):
    global position
    try:
        if 0<=int(text) and int(text)<=999:
            (x,y) = position
            canvas.create_oval(x-half_node_size, y-half_node_size, x+half_node_size, y+half_node_size, fill='light green')
            canvas.create_text(x,y,fill="darkblue",text=text)
            canvas.create_line(x+half_node_size,y,x+node_size*1.5-half_node_size,y,fill='green')
            position = (x+node_size*1.5,y)
            i.config(text='')
        else:
            raise ValueError
    except ValueError:
        i.config(text="Now a valid input (int in range 0-999)")


frame = tk.Frame(r.frame)
tk.Label(frame,text="List",bg='light green', height=2).pack(fill='x')
i = tk.Label(frame,pady=5)
e = tk.Entry(frame)
c = tk.Canvas(frame,width=400, height=400, bg="white")
b = tk.Button(frame,text="Draw text", command=lambda: draw_node(e.get(),c),pady=5)

e.pack()
b.pack()
i.pack()
c.pack()
tk.Button(frame,text='Back',command=lambda: r.show_frame(m.frame)).pack()
