import tkinter as tk
from tkinter import font
import root as r
import menu as m

class tnode():
    def __init__(self,a,b,text,x,y):
        self.a = a
        self.b = b
        self.text = text
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.text} [{self.a},{self.b}])"


position = (100,100)
node_size = 26
half_node_size = node_size/2
the_tree = []

def draw_node(text,canvas):
    global position
    try:
        if 0<=int(text) and int(text)<=999:
            (x,y) = position
            draw_1(x,y,text)
            canvas.create_line(x+half_node_size,y,x+node_size*1.5-half_node_size,y,fill='green')
            position = (x+node_size*1.5,y)
            i.config(text='')
        else:
            raise ValueError
    except ValueError:
        i.config(text="Now a valid input (int in range 0-999)")

def add_to_tree(text, canvas):
    the_tree.append(tnode(0,0,text,0,0))
    draw_tree()
    # print(the_tree)

def draw_1(x,y,text):
    c.create_oval(x-half_node_size, y-half_node_size, x+half_node_size, y+half_node_size, fill='light green')
    c.create_text(x,y,fill="darkblue",text=text)

def tree_h(number,nChildren):
    if number == 0:
        return 0
    p = 1
    c = number
    h = 0
    while c - nChildren**p > 0:
        c-= (nChildren**p)
        p += 1
        h+=1
    return h+1


def draw_tree():
    c.delete("all")
    x = 400
    y = 30
    draw_1(x,y,the_tree[0].text)
    the_tree[0].a = 0
    the_tree[0].b = 800
    the_tree[0].x = 400
    the_tree[0].y = 30
    l = len(the_tree)-1
    index = 0
    while l>0:
        if l >= 3:
            print('c1')
            dist = the_tree[index].b - the_tree[index].a
            a = dist/6
            beg = the_tree[index].a
            for i in range(1,4):
                node = the_tree[3*index + i]
                node.a = beg
                beg += 2*a
                node.b = beg
            for i in range(1,4):
                node = the_tree[3*index + i]
                parent = the_tree[index]
                node.x = node.a + (node.b - node.a)/2
                node.y = (tree_h(3*index + i,3)+1)*30
                c.create_line(node.x,node.y,parent.x,parent.y,fill='green')
                draw_1(node.a + (node.b - node.a)/2,(tree_h(3*index + i,3)+1)*30, node.text)
                draw_1(parent.a + (parent.b - parent.a)/2, (tree_h(index,3)+1)*30, parent.text)
            l -= 3
            index += 1
        elif l >= 2:
            print('c2')
            dist = the_tree[index].b - the_tree[index].a
            a = dist/4
            beg = the_tree[index].a
            for i in range(1,3):
                print(3*index + i)
                node = the_tree[3*index + i]
                node.a = beg
                beg += 2*a
                node.b = beg
            for i in range(1,3):
                node = the_tree[3*index + i]
                parent = the_tree[index]
                node.x = node.a + (node.b - node.a)/2
                node.y = (tree_h(3*index + i,3)+1)*30
                c.create_line(node.x,node.y,parent.x,parent.y,fill='green')
                draw_1(node.a + (node.b - node.a)/2,(tree_h(3*index + i,3)+1)*30, node.text)
                draw_1(parent.a + (parent.b - parent.a)/2, (tree_h(index,3)+1)*30, parent.text)
            l -= 2
            index += 1
        else:
            print('c3')
            print(index)
            print(3*index + 1)
            print(tree_h(index,3)+1)
            
            node = the_tree[3*index + 1]
            node.a = the_tree[index].a
            node.b = the_tree[index].b
            parent = the_tree[index]
            node.x = node.a + (node.b - node.a)/2
            node.y = (tree_h(3*index + 1,3)+1)*30
            c.create_line(node.x,node.y,parent.x,parent.y,fill='green')
            draw_1(node.a + (node.b - node.a)/2,(tree_h(3*index + 1,3)+1)*30, node.text)
            draw_1(parent.a + (parent.b - parent.a)/2, (tree_h(index,3)+1)*30, parent.text)
            l -= 1
            index +=1


frame = tk.Frame(r.frame)
tk.Label(frame,text="List",bg='light green', height=2).pack(fill='x')
i = tk.Label(frame,pady=5)
e = tk.Entry(frame)
c = tk.Canvas(frame,width=800, height=400, bg="white")
b = tk.Button(frame,text="Draw text", command=lambda: add_to_tree(e.get(),c),pady=5)

e.pack()
b.pack()
i.pack()
c.pack()
tk.Button(frame,text='Back',command=lambda: r.show_frame(m.frame)).pack()
