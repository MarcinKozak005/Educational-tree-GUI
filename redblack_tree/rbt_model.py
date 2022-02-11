import copy
import core.root as r


class RBTree:
    def __init__(self, view):
        self.root = None
        self.view = view

    def insert_value(self, val):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty')
            self.root = RBTree.RBNode(self, self.view.width // 2, self.view.y_space, val, 0, self.view.width, None)
            self.root.color = 'black'
            self.view.explanation.append(f'Added node {val}[black]')
        else:
            self.root.insert_value(val)
        self.view.info_label.config(text='')
        self.view.canvas_now.delete('all')
        self.view.draw_rb_tree(self.root, self.view.canvas_now)
        self.view.explanation_label.config(text=self.view.explanation.string, wraplength=400)
        self.view.explanation.reset()

    def clear(self):
        self.root = None

    class RBNode:
        def __init__(self, tree, x, y, val, l_edge, r_edge, parent):
            self.val = val
            self.left = RBTree.RBLeaf()
            self.right = RBTree.RBLeaf()
            self.parent = parent
            self.tree = tree
            # Canvas visualization connected
            self.x = x  # x-position of the node
            self.y = y  # y-position of the node
            self.l_edge = l_edge  # edges for nice tree visualization
            self.r_edge = r_edge  # edges for nice tree visualization
            self.color = 'red'
            # Animation connected
            self.x_next = x
            self.y_next = y

        def __getitem__(self, item):
            if item == 'left':
                return self.left
            elif item == 'right':
                return self.right

        def __setitem__(self, key, value):
            if key == 'left':
                self.left = value
            elif key == 'right':
                self.right = value

        def successors(self):
            result = []
            if type(self.left) is RBTree.RBNode:
                result += self.left.successors()
            if type(self.right) is RBTree.RBNode:
                result += self.right.successors()
            result.append(self)
            return result

        def insert_value(self, val):  # dawniej rb_tree_root_insert
            view = self.tree.view
            view.explanation.append(f'Tree is not empty, looking for insert place for {val}')
            view.canvas_now.create_oval(self.tree.root.x - view.half_node_size,
                                        self.tree.root.y - view.y_above - view.half_node_size,
                                        self.tree.root.x + view.half_node_size,
                                        self.tree.root.y - view.y_above + view.half_node_size,
                                        fill='grey', tags=f'grey_node')
            view.canvas_now.create_text(self.tree.root.x, self.tree.root.y - view.y_above, fill='white', text=val,
                                        tags=f'grey_node')
            newNode = self.tree.root.subtree_insert_value(val)
            view.draw_exp_text(newNode, f'Inserting {newNode.val}', False)
            view.explanation.append(f'{val} inserted. Starting fixing')
            view.draw_subtree(newNode, view.canvas_now)
            view.canvas_now.delete('grey_node')
            view.draw_line(view.canvas_now, newNode, newNode.parent, tags=[f'Line{newNode.__hash__()}', 'Line'])
            view.canvas_now.tag_lower(f'Line{newNode.__hash__()}')
            newNode.fix_insert()
            view.explanation.append(f'Fixing finished')

        # Metoda klasy z RBTree-TBNode
        def subtree_insert_value(self, val):  # dawniej rb_subtree_insert
            view = self.tree.view
            unit = (self.r_edge - self.l_edge) / 4
            if val >= self.val and type(self.right) == RBTree.RBNode:  # funkcja do sprawdzanai?
                view.draw_exp_text(self, f'{val} >= {self.val} --> choosing right subtree', False)
                view.move_object('grey_node', self.x, self.y - view.half_node_size - view.y_above, self.right.x,
                                 self.right.y - view.half_node_size - view.y_above)
                newNode = self.right.subtree_insert_value(val)
            elif val >= self.val:
                view.draw_exp_text(self, f'{val} >= {self.val} --> choosing right subtree', False)
                newNode = RBTree.RBNode(self.tree, self.x + unit, self.y + view.y_space, val, self.x, self.r_edge, self)
                self.right = newNode
                view.move_object('grey_node', self.x, self.y - view.half_node_size - view.y_above, self.right.x,
                                 self.right.y - view.half_node_size)
            elif val < self.val and type(self.left) == RBTree.RBNode:
                view.draw_exp_text(self, f'{val} < {self.val} --> choosing left subtree', False)
                view.move_object('grey_node', self.x, self.y - view.half_node_size - view.y_above, self.left.x,
                                 self.left.y - view.half_node_size - view.y_above)
                newNode = self.left.subtree_insert_value(val)
            else:
                view.draw_exp_text(self, f'{val} < {self.val} --> choosing left subtree', False)
                newNode = RBTree.RBNode(self.tree, self.x - unit, self.y + view.y_space, val, self.l_edge, self.x, self)
                self.left = newNode
                view.move_object('grey_node', self.x, self.y - view.half_node_size - view.y_above, self.left.x,
                                 self.left.y - view.half_node_size)
            return newNode

        def fix_rb_tree_insert_case1(self, y):
            view = self.tree.view
            self.parent.color = 'black'
            y.color = 'black'
            self.parent.parent.color = 'red'
            view.draw_recolor_text(self.parent, 'black')
            view.draw_recolor_text(y, 'black')
            view.draw_recolor_text(self.parent.parent, 'red')
            r.frame.update()
            r.frame.after(view.animation_time)
            view.draw_node(self.parent, view.canvas_now)
            view.draw_node(y, view.canvas_now)
            view.draw_node(self.parent.parent, view.canvas_now)
            view.canvas_now.delete('recolor_txt')

        def fix_rb_tree_insert_half(self, side):
            node = self
            view = self.tree.view
            y = node.parent.parent['right' if side == 'left' else 'left']
            if y.color == 'red':
                node.fix_rb_tree_insert_case1(y)
                return node.parent.parent
            elif node == node.parent['right' if side == 'left' else 'left']:
                node = node.parent
                node.rotate(side)
            elif node is not self.tree.root and node.parent is not self.tree.root:
                node.parent.color = 'black'
                node.parent.parent.color = 'red'
                tmp_node1, tmp_node2 = node.parent, node.parent.parent
                node.parent.parent.rotate('right' if side == 'left' else "left")
                view.draw_recolor_text(tmp_node1, 'black')
                view.draw_recolor_text(tmp_node2, 'red')
                r.frame.update()
                r.frame.after(view.animation_time)
                view.draw_node(tmp_node1, view.canvas_now)
                view.draw_node(tmp_node2, view.canvas_now)
                view.canvas_now.delete('recolor_txt')
            return node

        # Based on Thomas Cormen's Intro. to Algorithms
        def fix_insert(self):  # dawniej fix_rb_tree_insert
            node = self
            view = self.tree.view
            while node is not self.tree.root and node.parent.color == 'red':
                if node.parent == node.parent.parent.left:
                    node = node.fix_rb_tree_insert_half('left')
                else:
                    node = node.fix_rb_tree_insert_half('right')
            if self.tree.root.color != 'black':
                view.draw_recolor_text(self.tree.root, 'black')
                r.frame.update()
                r.frame.after(view.animation_time)
            self.tree.root.color = 'black'

        # Based on Thomas Cormen's Intro. to Algorithms
        def rotate(self, side):
            view = self.tree.view
            view.draw_exp_text(self, f'{side}-rotate on {self.val}')
            y = self['right' if side == 'left' else 'left']
            self['right' if side == 'left' else 'left'] = y[side]
            if type(y[side]) != RBTree.RBLeaf:
                y[side].parent = self
                # print(f'lr-1 {self.val}')
            y.parent = self.parent
            if self.parent is None:
                self.tree.root = y
                # print(f'lr-2 {self.val}')
            elif self == self.parent[side]:
                self.parent[side] = y
                # print(f'lr-3 {self.val}')
            else:
                self.parent['right' if side == 'left' else 'left'] = y
                # print(f'lr-4 {self.val}')
            y[side] = self
            self.parent = y
            self.update_positions(self.tree.root)
            view.animate_rotations(y)

        # Cavas vizualisation - place nodes in correct spots
        # self a node?
        def update_positions(self, node, static=False, width=None):
            view = self.tree.view
            if type(node) is RBTree.RBNode and node.parent is not None:
                # node is not self.tree.root and node is not self.tree.root_copy
                unit = (node.parent.r_edge - node.parent.l_edge) / 4
                if node is node.parent.right:
                    node.x_next = node.parent.x_next + unit
                    node.y_next = node.parent.y_next + view.y_space
                    node.l_edge = node.parent.x_next
                    node.r_edge = node.parent.r_edge
                elif node is node.parent.left:
                    node.x_next = node.parent.x_next - unit
                    node.y_next = node.parent.y_next + view.y_space
                    node.l_edge = node.parent.l_edge
                    node.r_edge = node.parent.x_next
            elif type(node) is RBTree.RBNode and node.parent is None:
                # (node is self.tree.root or node is self.tree.root_copy)
                node.x_next = view.width // 2 if width is None else width // 2
                node.y_next = view.y_space
                node.l_edge = 0
                node.r_edge = view.width if width is None else width
            if type(node) is RBTree.RBNode and static:
                node.x = node.x_next
                node.y = node.y_next
            if type(node) is RBTree.RBNode:
                # print(f'Post: {node.val} -- [{node.x},{node.y}] {node.l_edge}|{node.r_edge}')
                self.update_positions(node.left, static)
                self.update_positions(node.right, static)

        def rb_tree_root_delete(self, text):
            view = self.tree.view
            view.set_buttons(False)
            node = self.rb_tree_root_find(text, False)
            if text.isdigit() and 0 <= int(text) <= 999:
                if type(node) is not RBTree.RBNode:
                    view.info_label.config(text=f'There is no element \'{text}\' in the tree')
                else:
                    if node is self.tree.root and type(node.left) is RBTree.RBLeaf and type(
                            node.right) is RBTree.RBLeaf:
                        view.canvas_now.delete('hint_frame')
                        view.move_object(f'Node{self.tree.root.__hash__()}', self.tree.root.x, self.tree.root.y,
                                         self.tree.root.x,
                                         -view.node_size)
                        self.tree.root = None
                        view.info_label.config(text='')
                        view.canvas_now.delete('all')
                        # view.canvas_prev.delete('all')
                        # view.draw_rb_tree(rb_tree_root_copy, view.canvas_prev)
                        view.explanation_label.config(text=view.explanation.string, wraplength=400)
                        view.explanation.reset()
                        view.set_buttons(True)
                        return
                    if type(node.left) is RBTree.RBLeaf or type(node.right) is RBTree.RBLeaf:
                        view.explanation.append(f'Right or left child of {node.val} is a leaf')
                        y = node
                    else:
                        view.draw_exp_text(node, f'Looking for the successor of {node.val}')
                        y = self.tree_successor(node)
                    if type(y.left) is not RBTree.RBLeaf:
                        x = y.left
                    else:
                        x = y.right
                    x.parent = y.parent
                    if y.parent is None:
                        self.tree.root = x
                    elif y == y.parent.left:
                        y.parent.left = x
                    else:
                        y.parent.right = x
                    view.canvas_now.delete(f'Line{y.__hash__()}')
                    view.canvas_now.delete('hint_frame')
                    self.update_positions(self.tree.root)
                    if y is not node:
                        view.explanation.append(f'Swap {node.val} with {y.val}')
                        view.canvas_now.create_oval(node.x - view.half_node_size, node.y - view.half_node_size,
                                                    node.x + view.half_node_size,
                                                    node.y + view.half_node_size, fill=node.color, tags='swap1')
                        view.canvas_now.create_oval(y.x - view.half_node_size, y.y - view.half_node_size,
                                                    y.x + view.half_node_size,
                                                    y.y + view.half_node_size, fill=y.color, tags=f'Node{y.__hash__()}')
                        txt1 = view.canvas_now.create_text(node.x, node.y, fill='blue', text=node.val,
                                                           tags=[f'Node{y.__hash__()}', 'txt1'])
                        txt2 = view.canvas_now.create_text(y.x, y.y, fill='blue', text=y.val, tags=['swap1', 'txt2'])
                        txt1_bg = view.canvas_now.create_rectangle(view.canvas_now.bbox(txt1), fill='white',
                                                                   tags=[f'Node{y.__hash__()}', 'txt1'])
                        txt2_bg = view.canvas_now.create_rectangle(view.canvas_now.bbox(txt2), fill='white',
                                                                   tags=['swap1', 'txt2'])
                        view.canvas_now.tag_lower(txt1_bg, txt1)
                        view.canvas_now.tag_lower(txt2_bg, txt2)
                        view.move_object('txt1', node.x, node.y, y.x, y.y)
                        view.move_object('txt2', y.x, y.y, node.x, node.y)
                        node.val = y.val
                        view.canvas_now.delete('swap1')
                        view.draw_node(node, view.canvas_now)
                    view.move_object(f'Node{y.__hash__()}', y.x, y.y, y.x, - view.node_size)
                    if y.color == 'black':
                        self.fix_rb_tree_delete(x)
                        view.animate_rotations(self.tree.root)
                        view.draw_recolor_text(x, 'black')
                        r.frame.update()
                        r.frame.after(view.animation_time)
                        view.canvas_now.delete('recolor_txt')
                    view.info_label.config(text='')
                    view.canvas_now.delete('all')
                    # view.canvas_prev.delete('all')
                    view.explanation.append(f'Deletion finished')
                    view.draw_rb_tree(self.tree.root, view.canvas_now)
                    # view.draw_rb_tree(rb_tree_root_copy, view.canvas_prev)
                    view.explanation_label.config(text=view.explanation.string, wraplength=400)
                    view.explanation.reset()
                    if type(self.tree.root) is RBTree.RBLeaf or self.tree.root is None:
                        self.tree.root = None
                    view.set_buttons(True)
            else:
                view.info_label.config(text='DELETE: Not a valid input (integer in range 0-999)')
            view.set_buttons(True)

        def fix_rb_tree_delete(self, node):
            view = self.tree.view
            while node is not self.tree.root and node.color == 'black':
                if node == node.parent.left:
                    w = node.parent.right
                    if type(w) is not RBTree.RBLeaf and w.color == 'red':
                        w.color = 'black'
                        node.parent.color = 'red'
                        tmp_node1, tmp_node2 = w, node.parent
                        self.rotate(node.parent, 'left')
                        view.draw_recolor_text(tmp_node1, 'black')
                        view.draw_recolor_text(tmp_node2, 'red')
                        r.frame.update()
                        r.frame.after(view.animation_time)
                        view.draw_node(tmp_node1, view.canvas_now)
                        view.draw_node(tmp_node2, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        w = node.parent.right
                    if type(w) is not RBTree.RBLeaf and w.left.color == 'black' and w.right.color == 'black':
                        w.color = 'red'
                        view.draw_recolor_text(w, 'red')
                        r.frame.update()
                        r.frame.after(view.animation_time)
                        view.draw_node(w, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        node = node.parent
                    elif type(w) is not RBTree.RBLeaf and w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        tmp_node1, tmp_node2 = w.left, w
                        self.rotate(w, 'right')
                        view.draw_recolor_text(tmp_node1, 'black')
                        view.draw_recolor_text(tmp_node2, 'red')
                        r.frame.update()
                        r.frame.after(view.animation_time)
                        view.draw_node(tmp_node1, view.canvas_now)
                        view.draw_node(tmp_node2, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        w = node.parent.right
                    if node is not self.tree.root:
                        w.color = node.parent.color
                        node.parent.color = 'black'
                        w.right.color = 'black'
                        tmp_node1, tmp_node2, tmp_node3 = w, node.parent, w.right
                        if node.parent is not self.tree.root:
                            self.rotate(node.parent, 'left')
                        view.draw_recolor_text(tmp_node1, node.parent.color)
                        view.draw_recolor_text(tmp_node2, 'black')
                        view.draw_recolor_text(tmp_node3, 'black')
                        r.frame.update()
                        r.frame.after(view.animation_time)
                        view.draw_node(tmp_node1, view.canvas_now)
                        view.draw_node(tmp_node2, view.canvas_now)
                        view.draw_node(tmp_node3, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        node = self.tree.root
                else:
                    w = node.parent.left
                    if type(w) is not RBTree.RBLeaf and w.color == 'red':
                        w.color = 'black'
                        node.parent.color = 'red'
                        tmp_node1, tmp_node2 = w, node.parent
                        self.rotate(node.parent, 'right')
                        view.draw_recolor_text(tmp_node1, 'black')
                        view.draw_recolor_text(tmp_node2, 'red')
                        r.frame.update()
                        r.frame.after(view.animation_time)
                        view.draw_node(tmp_node1, view.canvas_now)
                        view.draw_node(tmp_node2, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        w = node.parent.left
                    if type(w) is not RBTree.RBLeaf and w.right.color == 'black' and w.left.color == 'black':
                        w.color = 'red'
                        view.draw_recolor_text(w, 'red')
                        r.frame.update()
                        r.frame.after(view.animation_time)
                        view.draw_node(w, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        node = node.parent
                    elif type(w) is not RBTree.RBLeaf and w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        tmp_node1, tmp_node2 = w.right, w
                        self.rotate(w, 'left')
                        view.draw_recolor_text(tmp_node1, 'black')
                        view.draw_recolor_text(tmp_node2, 'red')
                        r.frame.update()
                        r.frame.after(view.animation_time)
                        view.draw_node(tmp_node1, view.canvas_now)
                        view.draw_node(tmp_node2, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        w = node.parent.left
                    if node is not self.tree.root:  # Next
                        w.color = node.parent.color
                        node.parent.color = 'black'
                        w.left.color = 'black'
                        tmp_node1, tmp_node2, tmp_node3 = w, node.parent, w.left
                        if node.parent is not self.tree.root:
                            self.rotate(node.parent, 'right')
                        view.draw_recolor_text(tmp_node1, node.parent.color)
                        view.draw_recolor_text(tmp_node2, 'black')
                        view.draw_recolor_text(tmp_node3, 'black')
                        r.frame.update()
                        r.frame.after(view.animation_time)
                        view.draw_node(tmp_node1, view.canvas_now)
                        view.draw_node(tmp_node2, view.canvas_now)
                        view.draw_node(tmp_node3, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        node = self.tree.root
            node.color = 'black'

        def tree_successor(self, node):
            view = self.tree.view
            if type(node.right) is not RBTree.RBLeaf:
                view.move_object('hint_frame', node.x, node.y, node.right.x, node.right.y)
                view.draw_exp_text(node.right, f'Looking for the minimum of {node.right.val}')
                tmp = self.tree_minimum(node.right)
                return tmp
            y = node.parent
            while type(y) is not RBTree.RBLeaf and node is y.right:
                x = y
                y = x.parent
            view.explanation.append(f'{y.val}')
            return y

        def tree_minimum(self, tree):
            view = self.tree.view
            while type(tree.left) is not RBTree.RBLeaf:
                view.draw_exp_text(tree, f'{tree.val} has a left child ')
                view.move_object('hint_frame', tree.x, tree.y, tree.left.x, tree.left.y)
                tree = tree.left
            view.draw_exp_text(tree, f'Minimum found: {tree.val}')
            return tree

        def rb_tree_root_find(self, text, show_to_gui=True):
            view = self.tree.view
            view.set_buttons(False)
            if text.isdigit() and 0 <= int(text) <= 999:
                val = int(text)
                view.explanation.append(f'Looking for a node {val}')
                curr = self.tree.root
                view.canvas_now.create_rectangle(self.tree.root.x - view.half_node_size,
                                                 self.tree.root.y - view.half_node_size,
                                                 self.tree.root.x + view.half_node_size,
                                                 self.tree.root.y + view.half_node_size,
                                                 outline='red', tags='hint_frame')
                while type(curr) is not RBTree.RBLeaf and curr.val != val:
                    if curr.val > val and type(curr.left) is RBTree.RBNode:
                        view.draw_exp_text(curr, f'{val} < {curr.val}. Choosing left subtree')
                        view.move_object('hint_frame', curr.x, curr.y, curr.left.x, curr.left.y)
                        curr = curr.left
                    elif curr.val > val:
                        view.draw_exp_text(curr, f'{val} < {curr.val}. Choosing left subtree')
                        unit = (curr.r_edge - curr.l_edge) / 4
                        view.move_object('hint_frame', curr.x, curr.y, curr.x - unit, curr.y + view.y_space)
                        view.draw_exp_text(RBTree.RBNode(curr.x - unit, curr.y + view.y_space, None, None, None, None),
                                           'Element not found')
                        view.set_buttons(True)
                        view.canvas_now.delete('hint_frame')
                        return None
                    elif curr.val <= val and type(curr.right) is RBTree.RBNode:
                        view.draw_exp_text(curr, f'{val} >= {curr.val}. Choosing right subtree')
                        view.move_object('hint_frame', curr.x, curr.y, curr.right.x, curr.right.y)
                        curr = curr.right
                    elif curr.val <= val:
                        view.draw_exp_text(curr, f'{val} >= {curr.val}. Choosing right subtree')
                        unit = (curr.r_edge - curr.l_edge) / 4
                        view.move_object('hint_frame', curr.x, curr.y, curr.x + unit, curr.y + view.y_space)
                        view.draw_exp_text(RBTree.RBNode(curr.x + unit, curr.y + view.y_space, None, None, None, None),
                                           'Element not found')
                        view.set_buttons(True)
                        view.canvas_now.delete('hint_frame')
                        return None
                view.draw_exp_text(curr, f'{curr.val} found')
                if show_to_gui:
                    view.info_label.config(
                        text=f'Elem \'{text}\' found' if type(
                            curr) is not RBTree.RBLeaf else f'Elem \'{text}\' not found')
                    view.canvas_now.delete('hint_frame')
                else:
                    view.set_buttons(True)
                    return curr
            else:
                view.info_label.config(text='FIND: Not a valid input (integer in range 0-999)')
            view.set_buttons(True)

        def print_tree(self, tree, i=0):
            if type(tree) is RBTree.RBNode:
                print(' ' * i + f'{tree.val} - {tree.x}/{tree.y}')
                i += 1
                self.print_tree(tree.left, i)
                self.print_tree(tree.right, i)
                i -= 1

    class RBLeaf:
        color = 'black'

        def __init__(self):
            pass
