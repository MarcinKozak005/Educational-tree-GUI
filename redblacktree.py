import tkinter as tk
from tkinter import Label, font
from tkinter.constants import X
import root as r
import menu as m

class rb_node():
    def __init__(self,x,y,val,l_edge,r_edge,parent):
        self.val = val
        self.left = rb_leaf()
        self.right = rb_leaf()
        self.parent = parent
        # Canvas visualization connected
        self.x = x # x-position of the node
        self.y = y # y-position of the node
        self.l_edge = l_edge # edges for nice tree visualization
        self.r_edge = r_edge # edges for nice tree visualization
        self.color = "red"

class rb_leaf():
    color = 'black'
    def __init__(self):
        pass

rb_root_tree = None
y_space = 30
width = 800
node_size = 26
half_node_size = node_size/2

def clear():
    global rb_root_tree
    rb_root_tree = None
    canvas.delete("all")
    # print('########') # terminal visualization

def rb_subtree_add(val, tree):
    unit = (tree.r_edge - tree.l_edge)/4
    if val >= tree.val and type(tree.right) != rb_leaf:
        # print(f'add-1 {tree.val}')
        newNode = rb_subtree_add(val,tree.right)
    elif val >= tree.val:
        newNode = rb_node(tree.x + unit,tree.y + y_space,val,tree.x,tree.r_edge,tree)
        tree.right = newNode
        # print(f'add-2 {tree.val}')
    elif val < tree.val and type(tree.left) != rb_leaf:
        # print(f'add-3 {tree.val}')
        newNode = rb_subtree_add(val,tree.left)
    else:
        newNode = rb_node(tree.x - unit,tree.y + y_space,val,tree.l_edge,tree.x,tree)
        tree.left = newNode
        # print(f'add-4 {tree.val}')
    return newNode

def rb_root_tree_add(text,canvas):
    try:
        val = int(text)
        if 0 <= val and val <= 999:
            global rb_root_tree
            if rb_root_tree is None:
                rb_root_tree = rb_node(width//2,y_space,int(text),0,width,None)
                rb_root_tree.color = 'black'
                rb_root_tree.left = rb_leaf()
                rb_root_tree.right = rb_leaf()
            else:
                val = int(text) 
                newNode = rb_subtree_add(val,rb_root_tree)
                fix_rb_tree(newNode)
            label_input.config(text='')
            canvas.delete("all")
            draw_rb_tree(rb_root_tree,canvas)
        else:
            raise ValueError
    except ValueError:
        label_input.config(text="Now a valid input (int in range 0-999)")

    # Terminal visualization
    # print_tree(rb_root_tree)
    # print('-------')

# Based on Thomas Cormen's Intro. to Algorithms
def fix_rb_tree(node):
    while node is not rb_root_tree and node.parent.color == 'red':
        if node.parent == node.parent.parent.left:
            y = node.parent.parent.right
            if y.color == 'red':
                node.parent.color = 'black'
                y.color = 'black'
                node.parent.parent.color = 'red'
                node = node.parent.parent
                # print(f'fix-1 {node.val}')
            elif node == node.parent.right:
                node = node.parent
                left_rotate(node)
                # print(f'fix-2 {node.val}')
            elif node is not rb_root_tree and node.parent is not rb_root_tree:
                print(f'{node.val}-{node.parent.val}-{node.parent.parent.val}')
                node.parent.color = 'black'
                node.parent.parent.color = 'red'
                right_rotate(node.parent.parent)
                # print(f'fix-3 {node.val}')
        else:
            y = node.parent.parent.left
            if y.color == 'red':
                node.parent.color = 'black'
                y.color = 'black'
                node.parent.parent.color = 'red'
                node = node.parent.parent
                # print(f'fix-4 {node.val}')
            elif node == node.parent.left:
                node = node.parent
                right_rotate(node)
                # print(f'fix-5 {node.val}')
            elif node is not rb_root_tree and node.parent is not rb_root_tree:
                # print(f'{node.val}-{node.parent.val}-{node.parent.parent.val}')
                node.parent.color = 'black'
                node.parent.parent.color = 'red'
                left_rotate(node.parent.parent)
                # print(f'fix-6 {node.val}')
    rb_root_tree.color = 'black'

# Based on Thomas Cormen's Intro. to Algorithms
def left_rotate(node):
    global rb_root_tree
    y = node.right
    node.right = y.left
    if type(y.left) != rb_leaf:
        y.left.parent = node
        # print(f'lr-1 {node.val}')
    y.parent = node.parent
    if node.parent == None:
        rb_root_tree = y
        # print(f'lr-2 {node.val}')
    elif node == node.parent.left:
        node.parent.left = y
        # print(f'lr-3 {node.val}')
    else:
        node.parent.right = y
        # print(f'lr-4 {node.val}')
    y.left = node
    node.parent = y
    update_positions(y)


# Based on Thomas Cormen's Intro. to Algorithms
def right_rotate(node):
    global rb_root_tree
    y = node.left
    node.left = y.right
    if type(y.right) != rb_leaf:
        y.right.parent = node
        # print(f'rr-1 {node.val}')
    y.parent = node.parent
    if node.parent == None:
        rb_root_tree = y
        # print(f'rr-2 {node.val}')
    elif node == node.parent.right:
        node.parent.right = y
        # print(f'rr-3 {node.val}')
    else:
        node.parent.left = y
        # print(f'rr-4 {node.val}')
    y.right = node
    node.parent = y
    update_positions(y)

# Cavas vizualisation - place nodes in correct spots
def update_positions(node):
    if type(node) != rb_leaf and node is not rb_root_tree:
        unit = (node.parent.r_edge - node.parent.l_edge)/4
        if node is node.parent.right:
            node.x = node.parent.x + unit
            node.y = node.parent.y + y_space
            node.l_edge = node.parent.x
            node.r_edge = node.parent.r_edge
        elif node is node.parent.left:
            node.x = node.parent.x - unit
            node.y = node.parent.y + y_space
            node.l_edge = node.parent.l_edge
            node.r_edge = node.parent.x
    elif node is rb_root_tree:
        node.x = width//2
        node.y = y_space
        node.l_edge = 0
        node.r_edge = width
    if type(node) != rb_leaf:
        update_positions(node.left)
        update_positions(node.right)

# Canvas visualization
def draw_rb_tree(tree, canvas):
    if type(tree) is not rb_leaf:
        draw_rb_node(tree,canvas)
        draw_rb_tree(tree.left,canvas)
        draw_rb_tree(tree.right, canvas)

def draw_rb_node(node, canvas):
    if type(node) is not rb_leaf:
        if type(node.right) is not rb_leaf:
            canvas.create_line(node.x,node.y,node.right.x,node.right.y,fill='black')
        if type(node.left) is not rb_leaf:
            canvas.create_line(node.x,node.y,node.left.x,node.left.y,fill='black')
        canvas.create_oval(node.x-half_node_size, node.y-half_node_size, node.x+half_node_size, node.y+half_node_size, fill=node.color)
        canvas.create_text(node.x,node.y,fill="white",text=node.val)

# Terminal visualization
def print_tree(tree,i=0):
    if type(tree) is not rb_leaf:
        print(' '*i + f'{tree.val}')
        i += 1
        print_tree(tree.left,i)
        print_tree(tree.right,i)
        i -= 1


# GUI alignment
frame = tk.Frame(r.frame)
tk.Label(frame,text="RedBlack Tree",bg='red', height=2).pack(fill='x')
label_input = tk.Label(frame,pady=5)
entry_field = tk.Entry(frame)
canvas = tk.Canvas(frame,width=width, height=width//2, bg="white")
button_add = tk.Button(frame,text="Draw text", command=lambda: rb_root_tree_add(entry_field.get(),canvas),pady=5)
button_clear = tk.Button(frame,text="Clear", command=lambda:clear())

entry_field.pack()
button_add.pack()
button_clear.pack()
label_input.pack()
canvas.pack()
tk.Button(frame,text='Back',command=lambda: r.show_frame(m.frame)).pack()
    