import tkinter as tk
from tkinter import Label, font
from tkinter.constants import CURRENT, X
from typing import Collection
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

rb_tree_root = None
y_space = 30
width = 800
node_size = 26
half_node_size = node_size/2

def clear():
    global rb_tree_root
    rb_tree_root = None
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

def rb_tree_root_add(text,canvas):
    try:
        val = int(text)
        if 0 <= val and val <= 999:
            global rb_tree_root
            if rb_tree_root is None:
                rb_tree_root = rb_node(width//2,y_space,int(text),0,width,None)
                rb_tree_root.color = 'black'
                rb_tree_root.left = rb_leaf()
                rb_tree_root.right = rb_leaf()
            else:
                val = int(text) 
                newNode = rb_subtree_add(val,rb_tree_root)
                fix_rb_tree(newNode)
            label.config(text='')
            canvas.delete("all")
            draw_rb_tree(rb_tree_root,canvas)
        else:
            raise ValueError
    except ValueError:
        label.config(text="Now a valid input (int in range 0-999)")

    # Terminal visualization
    # print_tree(rb_tree_root)
    # print('-------')

# Based on Thomas Cormen's Intro. to Algorithms
def fix_rb_tree(node):
    while node is not rb_tree_root and node.parent.color == 'red':
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
            elif node is not rb_tree_root and node.parent is not rb_tree_root:
                # print(f'{node.val}-{node.parent.val}-{node.parent.parent.val}')
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
            elif node is not rb_tree_root and node.parent is not rb_tree_root:
                # print(f'{node.val}-{node.parent.val}-{node.parent.parent.val}')
                node.parent.color = 'black'
                node.parent.parent.color = 'red'
                left_rotate(node.parent.parent)
                # print(f'fix-6 {node.val}')
    rb_tree_root.color = 'black'

# Based on Thomas Cormen's Intro. to Algorithms
def left_rotate(node):
    global rb_tree_root
    y = node.right
    node.right = y.left
    if type(y.left) != rb_leaf:
        y.left.parent = node
        # print(f'lr-1 {node.val}')
    y.parent = node.parent
    if node.parent == None:
        rb_tree_root = y
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
    global rb_tree_root
    y = node.left
    node.left = y.right
    if type(y.right) != rb_leaf:
        y.right.parent = node
        # print(f'rr-1 {node.val}')
    y.parent = node.parent
    if node.parent == None:
        rb_tree_root = y
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
    if type(node) != rb_leaf and node is not rb_tree_root:
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
    elif node is rb_tree_root:
        node.x = width//2
        node.y = y_space
        node.l_edge = 0
        node.r_edge = width
    if type(node) != rb_leaf:
        update_positions(node.left)
        update_positions(node.right)


def rb_tree_root_delete(text):
    global rb_tree_root
    node = rb_tree_root_find(text,False)
    if type(node) is rb_leaf:
        label.config(text=f'There is no element \'{text}\' in the tree')
    else:
        if type(node.left) is rb_leaf or type(node.right) is rb_leaf:
            y = node
        else:
            y = tree_successor(node)
        if type(y.left) is not rb_leaf:
            x = y.left
        else:
            x = y.right
        x.parent = y.parent
        if y.parent is None:
            rb_tree_root = x
        elif y == y.parent.left: #Zmiana
            y.parent.left = x
        else:
            y.parent.right = x
        if y != node:
            node.val = y.val
            # node.x = y.x
            # node.y = y.y
            # node.l_edge = y.l_edge
            # node.r_edge = y.r_edge
        if y.color == 'black':
            fix_rb_tree_delete(x)
        label.config(text='')
        canvas.delete("all")
        update_positions(rb_tree_root)
        draw_rb_tree(rb_tree_root,canvas)
        if type(rb_tree_root) is rb_leaf:
            rb_tree_root = None
        return y

def fix_rb_tree_delete(node):
    while node is not rb_tree_root and node.color == 'black':
        if node == node.parent.left:
            w = node.parent.right
            if type(w) is not rb_leaf and w.color == 'red':
                w.color = 'black'
                node.parent.color = 'red'
                left_rotate(node.parent)
                w = node.parent.right
            if type(w) is not rb_leaf and w.left.color == 'black' and w.right.color == 'black':
                w.color = 'red'
                node = node.parent
            elif type(w) is not rb_leaf and w.right.color == 'black':
                w.left.color = 'black'
                w.color = 'red'
                right_rotate(w)
                w = node.parent.right
            if node is not rb_tree_root:
                w.color = node.parent.color
                node.parent.color = 'black'
                w.right.color = 'black'
                left_rotate(node.parent)
                node = rb_tree_root
        else:
            w = node.parent.left
            if type(w) is not rb_leaf and w.color == 'red':
                w.color = 'black'
                node.parent.color = 'red'
                right_rotate(node.parent)
                w = node.parent.left
            if type(w) is not rb_leaf and w.right.color == 'black' and w.left.color == 'black':
                w.color = 'red'
                node = node.parent
            elif type(w) is not rb_leaf and w.left.color == 'black':
                w.right.color = 'black'
                w.color = 'red'
                left_rotate(w)
                w = node.parent.left
            if node is not rb_tree_root: # Next
                w.color = node.parent.color
                node.parent.color = 'black'
                w.left.color = 'black'
                right_rotate(node.parent)
                node = rb_tree_root
    node.color = 'black'

def tree_successor(node):
    if type(node.right) is not rb_leaf:
        return tree_minimum(node.right)
    y = node.parent
    while type(y) is not rb_leaf and node == y.right:
        x = y
        y = x.parent
    return y

def tree_minimum(tree):
    while type(tree.left) is not rb_leaf:
        tree = tree.left
    return tree

def rb_tree_root_find(text,show_to_gui=True):
    # validacja
    val = int(text)
    curr = rb_tree_root
    while type(curr) is not rb_leaf and curr.val != val:
        if curr.val >= val:
            curr = curr.left
        elif curr.val < val:
            curr = curr.right
    if show_to_gui:
        label.config(text= f'Elem \'{text}\' found' if type(curr) is not rb_leaf else f'Elem \'{text}\' not found')
    else:
        return curr

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
canvas = tk.Canvas(frame,width=width, height=width//2, bg="white")
add_field = tk.Entry(frame)
add_button = tk.Button(frame,text="Draw text", command=lambda: rb_tree_root_add(add_field.get(),canvas),pady=5)
delete_field = tk.Entry(frame)
delete_button = tk.Button(frame, text="Delete", command=lambda: rb_tree_root_delete(delete_field.get()), pady=5)
find_field = tk.Entry(frame)
find_button = tk.Button(frame, text="Find", command=lambda: rb_tree_root_find(find_field.get(), canvas), pady=5)
clear_button = tk.Button(frame,text="Clear", command=lambda:clear())
label = tk.Label(frame,pady=5)

add_field.pack()
add_button.pack()
delete_field.pack()
delete_button.pack()
find_field.pack()
find_button.pack()
clear_button.pack()
label.pack()
canvas.pack()
tk.Button(frame,text='Back',command=lambda: r.show_frame(m.frame)).pack()
    