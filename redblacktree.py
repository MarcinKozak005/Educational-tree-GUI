import tkinter as tk
import core.root as r
import core.menu as m
import copy


class RBNode:
    def __init__(self, x, y, val, l_edge, r_edge, parent):
        self.val = val
        self.left = RBLeaf()
        self.right = RBLeaf()
        self.parent = parent
        # Canvas visualization connected
        self.x = x  # x-position of the node
        self.y = y  # y-position of the node
        self.l_edge = l_edge  # edges for nice tree visualization
        self.r_edge = r_edge  # edges for nice tree visualization
        self.color = "red"


class RBLeaf:
    color = 'black'

    def __init__(self):
        pass


class Explanation:
    string = ''
    line = 0

    def __init__(self):
        pass

    def append(self, text, newline=True):
        self.string += (f'[{self.line}] ' if newline else '') + f'{text}' + ('\n' if newline else '')
        self.line += 1

    def reset(self):
        self.string = ''
        self.line = 0


rb_tree_root = None
rb_tree_root_copy = None
explanation = Explanation()
y_space = 30
width = 800
height = 300
node_size = 26
half_node_size = node_size / 2
animation_time = 2000
animation_unit = 100


def clear():
    global rb_tree_root
    rb_tree_root = None
    canvas_prev.delete("all")
    canvas_now.delete("all")
    # print('########') # terminal visualization


def rb_subtree_add(val, tree):
    unit = (tree.r_edge - tree.l_edge) / 4
    if val >= tree.val and type(tree.right) != RBLeaf:
        explanation.append(f'{val} >= {tree.val}. Choosing right subtree')
        newNode = rb_subtree_add(val, tree.right)
    elif val >= tree.val:
        explanation.append(f'{val} >= {tree.val} and right({tree.val}) == null. Inserting {val} as right of {tree.val}')
        newNode = RBNode(tree.x + unit, tree.y + y_space, val, tree.x, tree.r_edge, tree)
        tree.right = newNode
    elif val < tree.val and type(tree.left) != RBLeaf:
        explanation.append(f'{val} < {tree.val}. Choosing left subtree')
        newNode = rb_subtree_add(val, tree.left)
    else:
        explanation.append(f'{val} < {tree.val} and left({tree.val}) == null. Inserting {val} as left of {tree.val}')
        newNode = RBNode(tree.x - unit, tree.y + y_space, val, tree.l_edge, tree.x, tree)
        tree.left = newNode
    return newNode


def rb_tree_root_add(text):
    global rb_tree_root_copy
    global rb_tree_root
    rb_tree_root_copy = copy.deepcopy(rb_tree_root)
    try:
        val = int(text)
        if 0 <= val <= 999:
            if rb_tree_root is None:
                explanation.append(f'Tree is empty')
                rb_tree_root = RBNode(width // 2, y_space, int(text), 0, width, None)
                rb_tree_root.color = 'black'
                rb_tree_root.left = RBLeaf()
                rb_tree_root.right = RBLeaf()
                explanation.append(f'Added node {val}[black]')
            else:
                val = int(text)
                explanation.append(f'Tree not empty, looking for insert place for {val}[red]')
                newNode = rb_subtree_add(val, rb_tree_root)
                explanation.append(f'{val}[black] inserted. Starting fixing')
                fix_rb_tree(newNode)
            label.config(text='')
            canvas_now.delete("all")
            canvas_prev.delete("all")
            draw_rb_tree(rb_tree_root, canvas_now)
            draw_rb_tree(rb_tree_root_copy, canvas_prev)
            explanation_label.config(text=explanation.string, wraplength=400)
            explanation.reset()
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
        explanation.append(f'{node.val} is not root and color({node.val}) == red, ', False)
        if node.parent == node.parent.parent.left:
            explanation.append(f'{node.parent.val} is left child of {node.parent.parent.val}, ', False)
            y = node.parent.parent.right
            if y.color == 'red':
                explanation.append(
                    f'uncle({node.val}) == {y.val}, color({y.val}) == red, recoloring {y.parent.val} and it\'s children'
                    + f' {node.parent.val} and {y.val}')
                node.parent.color = 'black'
                y.color = 'black'
                node.parent.parent.color = 'red'
                node = node.parent.parent
                # print(f'fix-1 {node.val}')
            elif node == node.parent.right:
                explanation.append(f'{node.val} is right child of {node.parent.val}. Left-rotate on {node.val}')
                node = node.parent
                left_rotate(node)
                # print(f'fix-2 {node.val}')
            elif node is not rb_tree_root and node.parent is not rb_tree_root:
                explanation.append(
                    f'Recolor {node.parent.val}, {node.parent.parent.val} and right-rotate on {node.parent.parent.val}')
                # print(f'{node.val}-{node.parent.val}-{node.parent.parent.val}')
                node.parent.color = 'black'
                node.parent.parent.color = 'red'
                right_rotate(node.parent.parent)
                # print(f'fix-3 {node.val}')
        else:
            explanation.append(f'{node.parent.val} is right child of {node.parent.parent.val}, ', False)
            y = node.parent.parent.left
            if y.color == 'red':
                explanation.append(
                    f'uncle({node.val}) == {y.val}, color({y.val}) == red, recoloring {y.parent.val} and it\'s children'
                    + f' {node.parent.val} and {y.val}')
                node.parent.color = 'black'
                y.color = 'black'
                node.parent.parent.color = 'red'
                node = node.parent.parent
                # print(f'fix-4 {node.val}')
            elif node == node.parent.left:
                explanation.append(f'{node.val} is left child of {node.parent.val}. Right-rotate on {node.val}')
                node = node.parent
                right_rotate(node)
                # print(f'fix-5 {node.val}')
            elif node is not rb_tree_root and node.parent is not rb_tree_root:
                explanation.append(
                    f'Recolor {node.parent.val}, {node.parent.parent.val} and left-rotate on {node.parent.parent.val}')
                # print(f'{node.val}-{node.parent.val}-{node.parent.parent.val}')
                node.parent.color = 'black'
                node.parent.parent.color = 'red'
                left_rotate(node.parent.parent)
                # print(f'fix-6 {node.val}')
    explanation.append(f'Set color({rb_tree_root.val}) = black')
    rb_tree_root.color = 'black'


# Based on Thomas Cormen's Intro. to Algorithms
def left_rotate(node):
    global rb_tree_root
    y = node.right
    node.right = y.left
    if type(y.left) != RBLeaf:
        y.left.parent = node
        # print(f'lr-1 {node.val}')
    y.parent = node.parent
    if node.parent is None:
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
    if type(y.right) != RBLeaf:
        y.right.parent = node
        # print(f'rr-1 {node.val}')
    y.parent = node.parent
    if node.parent is None:
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
    if type(node) != RBLeaf and node is not rb_tree_root:
        unit = (node.parent.r_edge - node.parent.l_edge) / 4
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
        node.x = width // 2
        node.y = y_space
        node.l_edge = 0
        node.r_edge = width
    if type(node) != RBLeaf:
        update_positions(node.left)
        update_positions(node.right)


def rb_tree_root_delete(text):
    global rb_tree_root
    global rb_tree_root_copy
    rb_tree_root_copy = copy.deepcopy(rb_tree_root)
    node = rb_tree_root_find(text, False)
    if type(node) is RBLeaf:
        label.config(text=f'There is no element \'{text}\' in the tree')
    else:
        explanation.append(f'{text} found')
        if type(node.left) is RBLeaf or type(node.right) is RBLeaf:
            explanation.append(f'right or left child of {node.val} is Null')
            y = node
        else:
            explanation.append(f'We are looking for the successor of {node.val}')
            y = tree_successor(node)
        if type(y.left) is not RBLeaf:
            x = y.left
        else:
            x = y.right
        x.parent = y.parent
        if y.parent is None:
            explanation.append(f'Change of the root {x.val}')
            rb_tree_root = x
        elif y == y.parent.left:
            y.parent.left = y
        else:
            y.parent.right = x
        if y != node:
            explanation.append(f'Swap of {node.val} and {y.val}')
            node.val = y.val
        if y.color == 'black':
            explanation.append(f'color({y.val}) == black, starting fixing for {x.val}')
            fix_rb_tree_delete(x)
        label.config(text='')
        canvas_now.delete("all")
        canvas_prev.delete("all")
        update_positions(rb_tree_root)
        draw_rb_tree(rb_tree_root, canvas_now)
        draw_rb_tree(rb_tree_root_copy, canvas_prev)
        explanation_label.config(text=explanation.string, wraplength=400)
        explanation.reset()
        if type(rb_tree_root) is RBLeaf or rb_tree_root is None:
            rb_tree_root = None
        return y


def fix_rb_tree_delete(node):
    while node is not rb_tree_root and node.color == 'black':
        if node == node.parent.left:
            w = node.parent.right
            if type(w) is not RBLeaf and w.color == 'red':
                w.color = 'black'
                node.parent.color = 'red'
                left_rotate(node.parent)
                w = node.parent.right
            if type(w) is not RBLeaf and w.left.color == 'black' and w.right.color == 'black':
                w.color = 'red'
                node = node.parent
            elif type(w) is not RBLeaf and w.right.color == 'black':
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
            if type(w) is not RBLeaf and w.color == 'red':
                w.color = 'black'
                node.parent.color = 'red'
                right_rotate(node.parent)
                w = node.parent.left
            if type(w) is not RBLeaf and w.right.color == 'black' and w.left.color == 'black':
                w.color = 'red'
                node = node.parent
            elif type(w) is not RBLeaf and w.left.color == 'black':
                w.right.color = 'black'
                w.color = 'red'
                left_rotate(w)
                w = node.parent.left
            if node is not rb_tree_root:  # Next
                w.color = node.parent.color
                node.parent.color = 'black'
                w.left.color = 'black'
                right_rotate(node.parent)
                node = rb_tree_root
    node.color = 'black'


def tree_successor(node):
    explanation.append(f'Successor of {node.val} is ', False)
    if type(node.right) is not RBLeaf:
        return tree_minimum(node.right)
    y = node.parent
    while type(y) is not RBLeaf and node == y.right:
        x = y
        y = x.parent
    explanation.append(f'{y.val}')
    return y


def tree_minimum(tree):
    explanation.append(f'Tree minimum of {tree.val} is ', False)
    while type(tree.left) is not RBLeaf:
        tree = tree.left
    explanation.append(f'{tree.val}')
    return tree


def rb_tree_root_find(text, show_to_gui=True):
    explanation.append(f'Looking for a node {text}')
    val = int(text)
    curr = rb_tree_root
    while type(curr) is not RBLeaf and curr.val != val:
        # path = draw_target_node(curr)
        if curr.val > val:
            curr = curr.left
            explanation.append(f'{val} < {curr.val}. Choosing left subtree')
        elif curr.val <= val:
            curr = curr.right
            explanation.append(f'{val} >= {curr.val}. Choosing right subtree')
    if show_to_gui:
        label.config(text=f'Elem \'{text}\' found' if type(curr) is not RBLeaf else f'Elem \'{text}\' not found')
    else:
        return curr


# Canvas visualization
def draw_rb_tree(tree, canvas):
    if type(tree) is not RBLeaf and tree is not None:
        draw_RBNode(tree, canvas)
        draw_rb_tree(tree.left, canvas)
        draw_rb_tree(tree.right, canvas)


def draw_RBNode(node, canvas):
    if type(node) is not RBLeaf:
        if type(node.right) is not RBLeaf:
            canvas.create_line(node.x, node.y, node.right.x, node.right.y, fill='black')
        if type(node.left) is not RBLeaf:
            canvas.create_line(node.x, node.y, node.left.x, node.left.y, fill='black')

        # canvas.create_oval(node.x - half_node_size, node.y - half_node_size, node.x + half_node_size,
        #                    node.y + half_node_size, fill=node.color,tags='a')
        # canvas.create_text(node.x, node.y, fill="white", text=node.val,tags='a')
        a = canvas.create_oval(0, 0, node_size,node_size, fill=node.color, tags=f'{node.__hash__()}')
        b = canvas.create_text(half_node_size, half_node_size, fill="white", text=node.val, tags=f'{node.__hash__()}')
        move_object(a, 0, 0, node.x, node.y)
        move_object(b, 0, 0, node.x, node.y)


def move_object(obj,x1,y1,x2,y2):
    x_diff = abs(x1-x2)
    y_diff = abs(y1-y2)
    x_unit = x_diff/(animation_time/animation_unit)
    y_unit = y_diff/(animation_time/animation_unit)
    move_tick(obj,x_unit,y_unit,animation_time/animation_unit)

def move_tick(obj,x_unit,y_unit,counter):
    if counter <= 0:
        return
    canvas_now.move(obj,x_unit,y_unit)
    frame.after(animation_unit,move_tick,obj,x_unit,y_unit,counter-1)

# Terminal visualization
def print_tree(tree, i=0):
    if type(tree) is not RBLeaf:
        print(' ' * i + f'{tree.val}')
        i += 1
        print_tree(tree.left, i)
        print_tree(tree.right, i)
        i -= 1


# GUI alignment
frame = tk.Frame(r.frame)

frame1 = tk.LabelFrame(frame, text='1')
tk.Label(frame1, text="RedBlack Tree", bg='red', height=2).pack(fill='x')
frame1.pack(fill='x')

frame2 = tk.LabelFrame(frame, text='2')
add_field = tk.Entry(frame2)
add_button = tk.Button(frame2, text="Add node", command=lambda: rb_tree_root_add(add_field.get()))
delete_field = tk.Entry(frame2)
delete_button = tk.Button(frame2, text="Delete node", command=lambda: rb_tree_root_delete(delete_field.get()))
find_field = tk.Entry(frame2)
find_button = tk.Button(frame2, text="Find node", command=lambda: rb_tree_root_find(find_field.get()))
clear_button = tk.Button(frame2, text="Clear tree", command=lambda: clear())
back_button = tk.Button(frame2, text='Back to menu', command=lambda: r.show_frame(m.frame))
label = tk.Label(frame2)
add_field.grid(row=0, column=0)
add_button.grid(row=0, column=1, padx=(0, 20))
delete_field.grid(row=0, column=2)
delete_button.grid(row=0, column=3, padx=(0, 20))
find_field.grid(row=0, column=4)
find_button.grid(row=0, column=5, padx=(0, 20))
clear_button.grid(row=0, column=6)
back_button.grid(row=0, column=7, padx=(40, 0))
label.grid(row=1, columnspan=6, sticky='WE')
frame2.pack()

frame3 = tk.LabelFrame(frame, text='3')
frame31 = tk.Frame(frame3)
explanation_title_lab = tk.Label(frame31)
explanation_label = tk.Label(frame31)
explanation_label.config(text='', justify=tk.LEFT, width=70, anchor=tk.W)
explanation_title_lab.config(text='Explanation', font=15)
explanation_title_lab.pack()
explanation_label.pack()
frame31.grid(row=0, column=0, sticky='NS')

frame32 = tk.Frame(frame3)
prev_label = tk.Label(frame32, text='Previous state of the tree:')
canvas_prev = tk.Canvas(frame32, width=width, height=height, bg="white")
now_label = tk.Label(frame32, text='Current state of the tree')
canvas_now = tk.Canvas(frame32, width=width, height=height, bg="white")
prev_label.pack(pady=(5, 0))
canvas_prev.pack()
now_label.pack(pady=(5, 0))
canvas_now.pack()
frame32.grid(row=0, column=1)
frame3.pack()
