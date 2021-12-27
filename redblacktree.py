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
        self.color = 'red'
        # Animation connected
        self.x_next = x
        self.y_next = y

    def successors(self):
        result = []
        if type(self.left) is RBNode:
            result += self.left.successors()
        if type(self.right) is RBNode:
            result += self.right.successors()
        result.append(self)
        return result


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
y_space = 50
y_above = 30
width = 800
height = 300
node_size = 26
half_node_size = node_size / 2
animation_time = 2000
animation_unit = 100


def clear():
    global rb_tree_root
    rb_tree_root = None
    canvas_prev.delete('all')
    canvas_now.delete('all')
    explanation_label.config(text='')


def draw_exp_text(node, exp_str, above=True):
    txt = canvas_now.create_text(node.x, node.y + (-1 if above else 1) * node_size, fill='white', text=exp_str, tags='exp_txt')
    txt_bg = canvas_now.create_rectangle(canvas_now.bbox(txt), fill="grey", tags='exp_txt')
    canvas_now.tag_lower(txt_bg)
    r.frame.update()
    r.frame.after(animation_time)
    canvas_now.delete('exp_txt')
    explanation.append(exp_str)


def draw_recolor_text(node,to_color):
    if type(node) is RBNode:
        txt = canvas_now.create_text(node.x, node.y - node_size, fill='white', text=f'Change color to {to_color}', tags='recolor_txt')
        txt_bg = canvas_now.create_rectangle(canvas_now.bbox(txt), fill="grey", tags='recolor_txt')
        canvas_now.tag_lower(txt_bg)


def rb_subtree_insert(val, tree):
    unit = (tree.r_edge - tree.l_edge) / 4
    if val >= tree.val and type(tree.right) == RBNode:
        exp_str = f'{val} >= {tree.val}. Choosing right subtree'
        draw_exp_text(tree, exp_str, False)
        move_object('grey_node', tree.x, tree.y - half_node_size - y_above, tree.right.x,
                    tree.right.y - half_node_size - y_above)
        newNode = rb_subtree_insert(val, tree.right)
    elif val >= tree.val:
        exp_str = f'{val} >= {tree.val} and right({tree.val}) == null. Inserting {val} as right of {tree.val}'
        draw_exp_text(tree, exp_str, False)
        newNode = RBNode(tree.x + unit, tree.y + y_space, val, tree.x, tree.r_edge, tree)
        tree.right = newNode
        move_object('grey_node', tree.x, tree.y - half_node_size - y_above, tree.right.x, tree.right.y - half_node_size)
    elif val < tree.val and type(tree.left) == RBNode:
        exp_str = f'{val} < {tree.val}. Choosing left subtree'
        draw_exp_text(tree, exp_str, False)
        move_object('grey_node', tree.x, tree.y - half_node_size - y_above, tree.left.x,
                    tree.left.y - half_node_size - y_above)
        newNode = rb_subtree_insert(val, tree.left)
    else:
        exp_str = f'{val} < {tree.val} and left({tree.val}) == null. Inserting {val} as left of {tree.val}'
        draw_exp_text(tree, exp_str, False)
        newNode = RBNode(tree.x - unit, tree.y + y_space, val, tree.l_edge, tree.x, tree)
        tree.left = newNode
        move_object('grey_node', tree.x, tree.y - half_node_size - y_above, tree.left.x, tree.left.y - half_node_size)
    draw_exp_text(newNode,'Inserting',False)
    return newNode


def rb_tree_root_insert(text):
    global rb_tree_root_copy
    global rb_tree_root
    set_buttons(False)
    rb_tree_root_copy = copy.deepcopy(rb_tree_root)

    if text.isdigit() and 0 <= int(text) <= 999:
        val = int(text)
        if rb_tree_root is None:
            explanation.append(f'Tree is empty')
            rb_tree_root = RBNode(width // 2, y_space, val, 0, width, None)
            rb_tree_root.color = 'black'
            explanation.append(f'Added node {val}[black]')
        else:
            explanation.append(f'Tree not empty, looking for insert place for {val}[red]')
            canvas_now.create_oval(rb_tree_root.x - half_node_size, rb_tree_root.y - y_above - half_node_size,
                                   rb_tree_root.x + half_node_size, rb_tree_root.y - y_above + half_node_size,
                                   fill='grey', tags=f'grey_node')
            canvas_now.create_text(rb_tree_root.x, rb_tree_root.y - y_above, fill='white', text=val, tags=f'grey_node')
            newNode = rb_subtree_insert(val, rb_tree_root)
            explanation.append(f'{val}[black] inserted. Starting fixing')
            draw_subtree(newNode, canvas_now)
            canvas_now.delete('grey_node')
            draw_line(canvas_now, newNode, newNode.parent, tags=[f'Line{newNode.__hash__()}', 'Line'])
            canvas_now.tag_lower(f'Line{newNode.__hash__()}')
            fix_rb_tree_insert(newNode)
        label.config(text='')
        canvas_now.delete('all')
        canvas_prev.delete('all')
        draw_rb_tree(rb_tree_root, canvas_now)
        draw_rb_tree(rb_tree_root_copy, canvas_prev)
        explanation_label.config(text=explanation.string, wraplength=400)
        explanation.reset()
    else:
        label.config(text='INSERT: Not a valid input (integer in range 0-999)')
    set_buttons(True)


# Based on Thomas Cormen's Intro. to Algorithms
def fix_rb_tree_insert(node):
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
                draw_recolor_text(node.parent, 'black')
                draw_recolor_text(y, 'black')
                draw_recolor_text(node.parent.parent, 'red')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(node.parent, canvas_now)
                draw_node(y, canvas_now)
                draw_node(node.parent.parent, canvas_now)
                canvas_now.delete('recolor_txt')
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
                tmp_node1, tmp_node2 = node.parent, node.parent.parent
                right_rotate(node.parent.parent)
                draw_recolor_text(tmp_node1,'black')
                draw_recolor_text(tmp_node2, 'red')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(tmp_node1, canvas_now)
                draw_node(tmp_node2, canvas_now)
                canvas_now.delete('recolor_txt')
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
                draw_recolor_text(node.parent, 'black')
                draw_recolor_text(y, 'black')
                draw_recolor_text(node.parent.parent, 'red')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(node.parent, canvas_now)
                draw_node(y, canvas_now)
                draw_node(node.parent.parent, canvas_now)
                canvas_now.delete('recolor_txt')
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
                tmp_node1, tmp_node2 = node.parent, node.parent.parent
                left_rotate(node.parent.parent)
                draw_recolor_text(tmp_node1,'black')
                draw_recolor_text(tmp_node2,'red')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(tmp_node1, canvas_now)
                draw_node(tmp_node2, canvas_now)
                canvas_now.delete('recolor_txt')
                # print(f'fix-6 {node.val}')
    explanation.append(f'Set color({rb_tree_root.val}) = black')
    if rb_tree_root.color != 'black':
        draw_recolor_text(rb_tree_root,'black')
        r.frame.update()
        r.frame.after(animation_time)
    rb_tree_root.color = 'black'


# Based on Thomas Cormen's Intro. to Algorithms
def left_rotate(node):
    draw_exp_text(node, f'Left-rotate on {node.val}')
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
    update_positions(rb_tree_root)
    animate_rotations(y)


def animate_rotations(node):
    successors = node.successors()
    units = {}
    tmp = animation_time / animation_unit
    for s in successors:
        x_unit = (s.x_next - s.x) / tmp
        y_unit = (s.y_next - s.y) / tmp
        units[s] = (x_unit, y_unit)
    while tmp > 0:
        for s in successors:
            rotation_tick(s, units[s][0], units[s][1])
        r.frame.after(animation_unit)
        r.frame.update()
        tmp -= 1


def rotation_tick(node, x_unit, y_unit):
    canvas_now.delete(f'Line{node.__hash__()}')
    canvas_now.delete(f'Line{node.parent.__hash__()}')
    canvas_now.move(f'Node{node.__hash__()}', x_unit, y_unit)
    node.x += x_unit
    node.y += y_unit
    draw_line(canvas_now, node, node.right, tags=[f'Line{node.__hash__()}', 'Line'])
    draw_line(canvas_now, node, node.left, tags=[f'Line{node.__hash__()}', 'Line'])
    if node.parent is not None:
        draw_line(canvas_now, node.parent, node.parent.right, tags=[f'Line{node.parent.__hash__()}', 'Line'])
        draw_line(canvas_now, node.parent, node.parent.left, tags=[f'Line{node.parent.__hash__()}', 'Line'])
    canvas_now.tag_lower('Line')


# Based on Thomas Cormen's Intro. to Algorithms
def right_rotate(node):
    draw_exp_text(node, f'Right-rotate on {node.val}')
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
    update_positions(rb_tree_root)
    animate_rotations(y)


# Cavas vizualisation - place nodes in correct spots
def update_positions(node):
    if type(node) is RBNode and node is not rb_tree_root:
        unit = (node.parent.r_edge - node.parent.l_edge) / 4
        if node is node.parent.right:
            node.x_next = node.parent.x_next + unit
            node.y_next = node.parent.y_next + y_space
            node.l_edge = node.parent.x_next
            node.r_edge = node.parent.r_edge
        elif node is node.parent.left:
            node.x_next = node.parent.x_next - unit
            node.y_next = node.parent.y_next + y_space
            node.l_edge = node.parent.l_edge
            node.r_edge = node.parent.x_next
    elif node is rb_tree_root:
        node.x_next = width // 2
        node.y_next = y_space
        node.l_edge = 0
        node.r_edge = width
    if type(node) is RBNode:
        # print(f'Post: {node.val} -- [{node.x},{node.y}] {node.l_edge}|{node.r_edge}')
        update_positions(node.left)
        update_positions(node.right)


def rb_tree_root_delete(text):
    global rb_tree_root
    global rb_tree_root_copy
    set_buttons(False)
    rb_tree_root_copy = copy.deepcopy(rb_tree_root)
    node = rb_tree_root_find(text, False)
    if text.isdigit() and 0 <= int(text) <= 999:
        if type(node) is not RBNode:
            label.config(text=f'There is no element \'{text}\' in the tree')
        else:
            explanation.append(f'{text} found')
            if node is rb_tree_root and type(node.left) is RBLeaf and type(node.right) is RBLeaf:
                move_object(f'Node{rb_tree_root.__hash__()}',rb_tree_root.x, rb_tree_root.y, rb_tree_root.x, 0)
                rb_tree_root = None
                label.config(text='')
                canvas_now.delete('all')
                canvas_prev.delete('all')
                draw_rb_tree(rb_tree_root_copy, canvas_prev)
                explanation_label.config(text=explanation.string, wraplength=400)
                explanation.reset()
                set_buttons(True)
                return
            if type(node.left) is RBLeaf or type(node.right) is RBLeaf:
                explanation.append(f'right or left child of {node.val} is Null')
                y = node
            else:
                draw_exp_text(node, f'We are looking for the successor of {node.val}')
                y = tree_successor(node)
            if type(y.left) is not RBLeaf:
                x = y.left
            else:
                x = y.right
            x.parent = y.parent
            if y.parent is None:
                explanation.append(f'Change of the root {x.val if type(x) is RBNode else ""}')
                rb_tree_root = x
            elif y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
            canvas_now.delete(f'Line{y.__hash__()}')
            update_positions(rb_tree_root)
            if y is not node:
                explanation.append(f'Swap of {node.val} and {y.val}')
                canvas_now.create_oval(node.x - half_node_size, node.y - half_node_size, node.x + half_node_size,
                                   node.y + half_node_size, fill=node.color, tags='swap1')
                canvas_now.create_oval(y.x - half_node_size, y.y - half_node_size, y.x + half_node_size,
                                       y.y + half_node_size, fill=y.color, tags='swap2')
                txt1 = canvas_now.create_text(node.x, node.y, fill='blue', text=node.val, tags='swap2')
                txt2 = canvas_now.create_text(y.x, y.y, fill='blue', text=y.val, tags='swap1')
                move_object(txt1, node.x, node.y, y.x, y.y)
                move_object(txt2, y.x, y.y, node.x, node.y)
                node.val = y.val
                canvas_now.delete('swap1')
                draw_node(node, canvas_now)
            move_object('swap2',y.x,y.y,y.x, 0)
            if y.color == 'black':
                explanation.append(
                    f'color({y.val if type(y) is RBNode else ""}) == black, starting fixing for {x.val if type(x) is RBNode else ""}')
                fix_rb_tree_delete(x)
                animate_rotations(rb_tree_root)
                draw_recolor_text(x,'black')
                r.frame.update()
                r.frame.after(animation_time)
                canvas_now.delete('recolor_txt')
            label.config(text='')
            canvas_now.delete('all')
            canvas_prev.delete('all')
            draw_rb_tree(rb_tree_root, canvas_now)
            draw_rb_tree(rb_tree_root_copy, canvas_prev)
            explanation_label.config(text=explanation.string, wraplength=400)
            explanation.reset()
            if type(rb_tree_root) is RBLeaf or rb_tree_root is None:
                rb_tree_root = None
            set_buttons(True)
    else:
        label.config(text='DELETE: Not a valid input (integer in range 0-999)')
    set_buttons(True)
    print_tree(rb_tree_root)


def fix_rb_tree_delete(node):
    while node is not rb_tree_root and node.color == 'black':
        if node == node.parent.left:
            w = node.parent.right
            if type(w) is not RBLeaf and w.color == 'red':
                w.color = 'black'
                node.parent.color = 'red'
                tmp_node1, tmp_node2 = w, node.parent
                left_rotate(node.parent)
                draw_recolor_text(tmp_node1, 'black')
                draw_recolor_text(tmp_node2, 'red')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(tmp_node1, canvas_now)
                draw_node(tmp_node2, canvas_now)
                canvas_now.delete('recolor_txt')
                w = node.parent.right
            if type(w) is not RBLeaf and w.left.color == 'black' and w.right.color == 'black':
                w.color = 'red'
                draw_recolor_text(w,'red')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(w, canvas_now)
                canvas_now.delete('recolor_txt')
                node = node.parent
            elif type(w) is not RBLeaf and w.right.color == 'black':
                w.left.color = 'black'
                w.color = 'red'
                tmp_node1, tmp_node2 = w.left, w
                right_rotate(w)
                draw_recolor_text(tmp_node1,'black')
                draw_recolor_text(tmp_node2,'red')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(tmp_node1, canvas_now)
                draw_node(tmp_node2, canvas_now)
                canvas_now.delete('recolor_txt')
                w = node.parent.right
            if node is not rb_tree_root:
                w.color = node.parent.color
                node.parent.color = 'black'
                w.right.color = 'black'
                tmp_node1, tmp_node2 = w, w.right
                left_rotate(node.parent)
                draw_recolor_text(tmp_node1, 'black')
                draw_recolor_text(tmp_node2, 'black')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(tmp_node1, canvas_now)
                draw_node(tmp_node2, canvas_now)
                canvas_now.delete('recolor_txt')
                node = rb_tree_root
        else:
            w = node.parent.left
            if type(w) is not RBLeaf and w.color == 'red':
                w.color = 'black'
                node.parent.color = 'red'
                tmp_node1, tmp_node2 = w, node.parent
                right_rotate(node.parent)
                draw_recolor_text(tmp_node1,'black')
                draw_recolor_text(tmp_node2,'red')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(tmp_node1, canvas_now)
                draw_node(tmp_node2, canvas_now)
                canvas_now.delete('recolor_txt')
                w = node.parent.left
            if type(w) is not RBLeaf and w.right.color == 'black' and w.left.color == 'black':
                w.color = 'red'
                draw_recolor_text(w,'red')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(w, canvas_now)
                canvas_now.delete('recolor_txt')
                node = node.parent
            elif type(w) is not RBLeaf and w.left.color == 'black':
                w.right.color = 'black'
                w.color = 'red'
                tmp_node1, tmp_node2 = w.right, w
                left_rotate(w)
                draw_recolor_text(tmp_node1, 'black')
                draw_recolor_text(tmp_node2,'red')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(tmp_node1, canvas_now)
                draw_node(tmp_node2, canvas_now)
                canvas_now.delete('recolor_txt')
                w = node.parent.left
            if node is not rb_tree_root:  # Next
                w.color = node.parent.color
                node.parent.color = 'black'
                w.left.color = 'black'
                tmp_node1, tmp_node2 = node.parent, w.left
                right_rotate(node.parent)
                draw_recolor_text(tmp_node1, 'black')
                draw_recolor_text(tmp_node2, 'black')
                r.frame.update()
                r.frame.after(animation_time)
                draw_node(tmp_node1, canvas_now)
                draw_node(tmp_node1, canvas_now)
                canvas_now.delete('recolor_txt')
                node = rb_tree_root
    node.color = 'black'


def tree_successor(node):
    explanation.append(f'Successor of {node.val} is ', False)
    if type(node.right) is not RBLeaf:
        move_object('hint_frame', node.x, node.y, node.right.x, node.right.y)
        draw_exp_text(node.right, f'Looking for the minimum of {node.right.val}')
        return tree_minimum(node.right)
    y = node.parent
    while type(y) is not RBLeaf and node is y.right:
        x = y
        y = x.parent
    explanation.append(f'{y.val}')
    return y


def tree_minimum(tree):
    explanation.append(f'Tree minimum of {tree.val} is ', False)
    while type(tree.left) is not RBLeaf:
        draw_exp_text(tree, f'{tree.val} has a left child ')
        move_object('hint_frame', tree.x, tree.y, tree.left.x, tree.left.y)
        tree = tree.left
    explanation.append(f'{tree.val}')
    draw_exp_text(tree, f'Minimum found:{tree.val}')
    return tree


def rb_tree_root_find(text, show_to_gui=True):
    set_buttons(False)
    if text.isdigit() and 0 <= int(text) <= 999:
        val = int(text)
        explanation.append(f'Looking for a node {val}')
        curr = rb_tree_root
        canvas_now.create_rectangle(rb_tree_root.x - half_node_size, rb_tree_root.y - half_node_size,
                                                 rb_tree_root.x + half_node_size, rb_tree_root.y + half_node_size,
                                                 outline='red', tags='hint_frame')
        while type(curr) is not RBLeaf and curr.val != val:
            if curr.val > val and type(curr.left) is RBNode:
                draw_exp_text(curr, f'{val} < {curr.val}. Choosing left subtree')
                move_object('hint_frame', curr.x, curr.y, curr.left.x, curr.left.y)
                curr = curr.left
            elif curr.val > val:
                draw_exp_text(curr, f'{val} < {curr.val}. Choosing left subtree')
                unit = (curr.r_edge - curr.l_edge) / 4
                move_object('hint_frame', curr.x, curr.y, curr.x - unit, curr.y + y_space)
                draw_exp_text(RBNode(curr.x - unit, curr.y + y_space,None, None,None,None), 'Element not found')
                set_buttons(True)
                canvas_now.delete('hint_frame')
                return None
            elif curr.val <= val and type(curr.right) is RBNode:
                draw_exp_text(curr, f'{val} >= {curr.val}. Choosing right subtree')
                move_object('hint_frame', curr.x, curr.y, curr.right.x, curr.right.y)
                curr = curr.right
            elif curr.val <= val:
                draw_exp_text(curr, f'{val} >= {curr.val}. Choosing right subtree')
                unit = (curr.r_edge - curr.l_edge) / 4
                move_object('hint_frame', curr.x, curr.y, curr.x + unit, curr.y + y_space)
                draw_exp_text(RBNode(curr.x + unit, curr.y + y_space,None, None,None,None), 'Element not found')
                set_buttons(True)
                canvas_now.delete('hint_frame')
                return None
        draw_exp_text(curr, 'Found')
        if show_to_gui:
            label.config(text=f'Elem \'{text}\' found' if type(curr) is not RBLeaf else f'Elem \'{text}\' not found')
            canvas_now.delete('hint_frame')
        else:
            set_buttons(True)
            return curr
    else:
        label.config(text='FIND: Not a valid input (integer in range 0-999)')
    set_buttons(True)


# Canvas visualization
def draw_rb_tree(tree, canvas):
    if type(tree) is not RBLeaf and tree is not None:
        draw_subtree(tree, canvas)
        draw_rb_tree(tree.left, canvas)
        draw_rb_tree(tree.right, canvas)


def draw_subtree(node, canvas):
    if type(node) is not RBLeaf:
        if type(node.right) is not RBLeaf:
            draw_line(canvas, node, node.right, tags=[f'Line{node.__hash__()}', 'Line'])
        if type(node.left) is not RBLeaf:
            draw_line(canvas, node, node.left, tags=[f'Line{node.__hash__()}', 'Line'])
        canvas.create_oval(node.x - half_node_size, node.y - half_node_size, node.x + half_node_size,
                           node.y + half_node_size, fill=node.color, tags=f'Node{node.__hash__()}')
        canvas.create_text(node.x, node.y, fill='white', text=node.val, tags=f'Node{node.__hash__()}')


def draw_node(node, canvas):
    if type(node) is RBNode:
        canvas.create_oval(node.x - half_node_size, node.y - half_node_size, node.x + half_node_size,
                           node.y + half_node_size, fill=node.color, tags=f'Node{node.__hash__()}')
        canvas.create_text(node.x, node.y, fill='white', text=node.val, tags=f'Node{node.__hash__()}')


def draw_line(canvas, node1, node2, tags=None):
    if node1 is not None and node2 is not None and type(node1) is not RBLeaf and type(node2) is not RBLeaf:
        canvas.create_line(node1.x, node1.y, node2.x, node2.y, fill='black', tags=tags)


def move_object(obj, x1, y1, x2, y2):
    x_diff = x2 - x1
    y_diff = y2 - y1
    x_unit = x_diff / (animation_time / animation_unit)
    y_unit = y_diff / (animation_time / animation_unit)
    counter = animation_time / animation_unit
    while counter > 0:
        canvas_now.move(obj, x_unit, y_unit)
        r.frame.update()
        canvas_now.after(animation_unit)
        counter -= 1


def print_tree(tree, i=0):
    if type(tree) is RBNode:
        print(' ' * i + f'{tree.val} - {tree.x}/{tree.y}')
        i += 1
        print_tree(tree.left, i)
        print_tree(tree.right, i)
        i -= 1


# GUI alignment
frame = tk.Frame(r.frame)

frame1 = tk.LabelFrame(frame, text='1')
tk.Label(frame1, text='RedBlack Tree', bg='red', height=2).pack(fill='x')
frame1.pack(fill='x')

frame2 = tk.LabelFrame(frame, text='2')
insert_field = tk.Entry(frame2)
insert_button = tk.Button(frame2, text='Add node', command=lambda: rb_tree_root_insert(insert_field.get()))
delete_field = tk.Entry(frame2)
delete_button = tk.Button(frame2, text='Delete node', command=lambda: rb_tree_root_delete(delete_field.get()))
find_field = tk.Entry(frame2)
find_button = tk.Button(frame2, text='Find node', command=lambda: rb_tree_root_find(find_field.get()))
clear_button = tk.Button(frame2, text='Clear tree', command=lambda: clear())
back_button = tk.Button(frame2, text='Back to menu', command=lambda: r.show_frame(m.frame))
label = tk.Label(frame2)
insert_field.grid(row=0, column=0)
insert_button.grid(row=0, column=1, padx=(0, 20))
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
canvas_prev = tk.Canvas(frame32, width=width, height=height, bg='white')
now_label = tk.Label(frame32, text='Current state of the tree')
canvas_now = tk.Canvas(frame32, width=width, height=height, bg='white')
prev_label.pack(pady=(5, 0))
canvas_prev.pack()
now_label.pack(pady=(5, 0))
canvas_now.pack()
frame32.grid(row=0, column=1)
frame3.pack()

buttons = [insert_button,delete_button,find_button,clear_button]

def set_buttons(val):
    for b in buttons:
        b.config(state='normal' if val else 'disabled')
