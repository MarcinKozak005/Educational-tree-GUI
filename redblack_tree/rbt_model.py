import core.root as r


class RBTree:
    def __init__(self, view):
        self.root = None
        self.view = view

    def insert_value(self, value):
        """
        Inserts value into the tree (into self.root)
        :param value: value being inserted
        :return: returns nothing
        """
        if self.root is None:
            self.root = RBTree.RBNode(self, self.view.width // 2, self.view.y_space, value, 0, self.view.width, None)
            self.root.color = 'black'
            self.view.explanation.append(f'Tree is empty')
            self.view.explanation.append(f'Added node {value}[black]')
        else:
            self.root.insert_value(value)

    def delete_value(self, value):
        """
        Deletes the value from the tree
        :param value: value to be deleted
        :return: returns nothing
        """
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to delete form empty tree')
        else:
            self.root.delete_value(value)

    def search_value(self, value):
        """
        Looks for the value in the tree. Shows the process in the GUI
        :param value: value to be found
        :return: returns nothing
        """
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Value cannot be found')
        else:
            self.root.search_value(value)

    def search_value_no_GUI(self, value):
        """
        Looks for the value in the tree.
        :param value: value to be found
        :return: found node or None
        """
        return self.root.search_value_no_GUI(value)

    def clear(self):
        """
        Resets self.root
        :return: returns nothing
        """
        self.root = None

    def print_tree(self):
        """
        Prints tree to the terminal
        :return: returns nothing
        """
        self.root.print_node()

    class RBLeaf:
        color = 'black'

        def __init__(self):
            pass

        def update_positions(self, static=None):
            pass

        def successors(self):
            return []

        def print_node(self, i):
            pass

    class RBNode:
        def __init__(self, tree, x, y, value, l_edge, r_edge, parent):
            self.value = value
            self.left = RBTree.RBLeaf()
            self.right = RBTree.RBLeaf()
            self.parent = parent
            self.tree = tree
            # Canvas visualization connected
            self.x = x  # x-position of the node
            self.y = y  # y-position of the node
            self.l_edge = l_edge  # edges for nice visualization
            self.r_edge = r_edge  # edges for nice visualization
            self.color = 'red'
            # Animation connected
            self.x_next = x
            self.y_next = y

        def __getitem__(self, item):
            """
            Enables to get self.left with self['left'] and self.right with self['right']
            :param item: string: 'left' or 'right'
            :return: self.left or self.right
            """
            if item == 'left':
                return self.left
            elif item == 'right':
                return self.right

        def __setitem__(self, key, value):
            """
            Enables to set self.left with self['left']=value and self.right with self['right']=value
            :param key: string: 'left' or 'right'
            :param value: new value of the attribute
            :return: returns nothing
            """
            if key == 'left':
                self.left = value
            elif key == 'right':
                self.right = value

        def successors(self):
            """
            Get the list of all successor nodes (children, children of children etc)
            :return: list of successors
            """
            result = []
            result += self.left.successors()
            result += self.right.successors()
            result.append(self)
            return result

        def insert_value(self, value):
            """
            Inserts value into the node
            :param value: value to insert
            :return: returns nothing
            """
            view = self.tree.view
            view.explanation.append(f'Tree is not empty, looking for insert place for {value}')
            view.canvas_now.create_oval(self.tree.root.x - view.half_node_size,
                                        self.tree.root.y - view.y_above - view.half_node_size,
                                        self.tree.root.x + view.half_node_size,
                                        self.tree.root.y - view.y_above + view.half_node_size,
                                        fill='grey', tags=f'grey_node')
            view.canvas_now.create_text(self.tree.root.x, self.tree.root.y - view.y_above, fill='white', text=value,
                                        tags=f'grey_node')
            newNode = self.tree.root.subtree_insert_value(value)
            view.draw_exp_text(newNode, f'Inserting {newNode.value}', False)
            view.explanation.append(f'{value} inserted. Starting fixing')
            view.draw_subtree(newNode, view.canvas_now)
            view.canvas_now.delete('grey_node')
            view.draw_line(view.canvas_now, newNode, newNode.parent, tags=[f'Line{newNode.__hash__()}', 'Line'])
            view.canvas_now.tag_lower(f'Line{newNode.__hash__()}')
            newNode.fix_insert()

        def subtree_insert_value(self, value):
            """
            Looks for the place to insert new value
            :param value: value to be inserted
            :return: reference to the inserted node
            """
            view = self.tree.view
            unit = (self.r_edge - self.l_edge) / 4
            if value >= self.value and type(self.right) is RBTree.RBNode:
                view.draw_exp_text(self, f'{value} >= {self.value} --> choosing right subtree', False)
                view.move_object('grey_node', self.x, self.y - view.half_node_size - view.y_above, self.right.x,
                                 self.right.y - view.half_node_size - view.y_above)
                newNode = self.right.subtree_insert_value(value)
            elif value >= self.value:
                view.draw_exp_text(self, f'{value} >= {self.value} --> choosing right subtree', False)
                newNode = RBTree.RBNode(self.tree, self.x + unit, self.y + view.y_space, value, self.x, self.r_edge,
                                        self)
                self.right = newNode
                view.move_object('grey_node', self.x, self.y - view.half_node_size - view.y_above, self.right.x,
                                 self.right.y - view.half_node_size)
            elif value < self.value and type(self.left) is RBTree.RBNode:
                view.draw_exp_text(self, f'{value} < {self.value} --> choosing left subtree', False)
                view.move_object('grey_node', self.x, self.y - view.half_node_size - view.y_above, self.left.x,
                                 self.left.y - view.half_node_size - view.y_above)
                newNode = self.left.subtree_insert_value(value)
            else:
                view.draw_exp_text(self, f'{value} < {self.value} --> choosing left subtree', False)
                newNode = RBTree.RBNode(self.tree, self.x - unit, self.y + view.y_space, value, self.l_edge, self.x,
                                        self)
                self.left = newNode
                view.move_object('grey_node', self.x, self.y - view.half_node_size - view.y_above, self.left.x,
                                 self.left.y - view.half_node_size)
            return newNode

        def fix_insert(self):
            """
            Fixes the red-black subtree starting in self after the insertion process
            :return: returns nothing
            """
            node = self
            view = self.tree.view

            def fix_insert_subpart(n, side):
                """
                fix_insert(self) subpart which is dependent on the side
                :param n: node to start the fixing subprocess
                :param side: string: 'left' or 'right'
                :return: node to continue fixing process
                """
                y = n.parent.parent['right' if side == 'left' else 'left']
                if y.color == 'red':
                    n.parent.color = 'black'
                    y.color = 'black'
                    n.parent.parent.color = 'red'
                    view.draw_recolor_text(n.parent, 'black')
                    view.draw_recolor_text(y, 'black')
                    view.draw_recolor_text(n.parent.parent, 'red')
                    r.wait(view.animation_time)
                    view.draw_node(n.parent, view.canvas_now)
                    view.draw_node(y, view.canvas_now)
                    view.draw_node(n.parent.parent, view.canvas_now)
                    view.canvas_now.delete('recolor_txt')
                    return n.parent.parent
                elif n == n.parent['right' if side == 'left' else 'left']:
                    n = n.parent
                    n.rotate(side)
                elif n is not self.tree.root and n.parent is not self.tree.root:
                    n.parent.color = 'black'
                    n.parent.parent.color = 'red'
                    tmp_node1, tmp_node2 = n.parent, n.parent.parent
                    n.parent.parent.rotate('right' if side == 'left' else "left")
                    view.draw_recolor_text(tmp_node1, 'black')
                    view.draw_recolor_text(tmp_node2, 'red')
                    r.wait(view.animation_time)
                    view.draw_node(tmp_node1, view.canvas_now)
                    view.draw_node(tmp_node2, view.canvas_now)
                    view.canvas_now.delete('recolor_txt')
                return n

            while node is not self.tree.root and node.parent.color == 'red':
                if node.parent == node.parent.parent.left:
                    node = fix_insert_subpart(node, 'left')
                else:
                    node = fix_insert_subpart(node, 'right')
            if self.tree.root.color != 'black':
                view.draw_recolor_text(self.tree.root, 'black')
                r.wait(view.animation_time)
            self.tree.root.color = 'black'
            view.explanation.append(f'Fixing finished')

        def rotate(self, side):
            """
            Perform the left or right rotate operation
            :param side: string: 'left' or 'right'
            :return: returns nothing
            """
            view = self.tree.view
            view.draw_exp_text(self, f'{side}-rotate on {self.value}')
            y = self['right' if side == 'left' else 'left']
            self['right' if side == 'left' else 'left'] = y[side]
            if type(y[side]) is not RBTree.RBLeaf:
                y[side].parent = self
            y.parent = self.parent
            if self.parent is None:
                self.tree.root = y
            elif self == self.parent[side]:
                self.parent[side] = y
            else:
                self.parent['right' if side == 'left' else 'left'] = y
            y[side] = self
            self.parent = y
            self.tree.root.update_positions()
            view.animate_rotations(y)

        def update_positions(self, static=False, width=None):
            """
            Updates the node's positions
            :param static: True means there will be no animation, False means there will be an animation
            :param width: width of canvas for updating positions
            :return: returns nothing
            """
            view = self.tree.view
            if self.parent is not None:
                unit = (self.parent.r_edge - self.parent.l_edge) / 4
                if self is self.parent.right:
                    self.x_next = self.parent.x_next + unit
                    self.y_next = self.parent.y_next + view.y_space
                    self.l_edge = self.parent.x_next
                    self.r_edge = self.parent.r_edge
                elif self is self.parent.left:
                    self.x_next = self.parent.x_next - unit
                    self.y_next = self.parent.y_next + view.y_space
                    self.l_edge = self.parent.l_edge
                    self.r_edge = self.parent.x_next
            elif self.parent is None:
                self.x_next = view.width // 2 if width is None else width // 2
                self.y_next = view.y_space
                self.l_edge = 0
                self.r_edge = view.width if width is None else width
            if static:
                self.x = self.x_next
                self.y = self.y_next
            self.left.update_positions(static)
            self.right.update_positions(static)

        def delete_value(self, value):
            """
            Deletes the value from the node or subnodes
            :param value: value to be deleted
            :return: returns nothing
            """
            view = self.tree.view
            node = self.search_value(value, False)
            if type(node) is not RBTree.RBNode:
                view.info_label.config(text=f'There is no element \'{value}\' in the tree')
                return
            else:
                if node is self.tree.root and type(node.left) is RBTree.RBLeaf and type(node.right) is RBTree.RBLeaf:
                    view.canvas_now.delete('hint_frame')
                    view.move_object(f'Node{self.tree.root.__hash__()}', self.tree.root.x, self.tree.root.y,
                                     self.tree.root.x,
                                     -view.node_size)
                    self.tree.clear()
                    return
                if type(node.left) is RBTree.RBLeaf or type(node.right) is RBTree.RBLeaf:
                    view.explanation.append(f'Right or left child of {node.value} is a leaf')
                    y = node
                else:
                    view.draw_exp_text(node, f'Looking for the successor of {node.value}')
                    y = node.successor()
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
                self.tree.root.update_positions()
                if y is not node:
                    view.explanation.append(f'Swap {node.value} with {y.value}')
                    view.canvas_now.create_oval(node.x - view.half_node_size, node.y - view.half_node_size,
                                                node.x + view.half_node_size,
                                                node.y + view.half_node_size, fill=node.color, tags='swap1')
                    view.canvas_now.create_oval(y.x - view.half_node_size, y.y - view.half_node_size,
                                                y.x + view.half_node_size,
                                                y.y + view.half_node_size, fill=y.color, tags=f'Node{y.__hash__()}')
                    txt1 = view.canvas_now.create_text(node.x, node.y, fill='blue', text=node.value,
                                                       tags=[f'Node{y.__hash__()}', 'txt1'])
                    txt2 = view.canvas_now.create_text(y.x, y.y, fill='blue', text=y.value, tags=['swap1', 'txt2'])
                    txt1_bg = view.canvas_now.create_rectangle(view.canvas_now.bbox(txt1), fill='white',
                                                               tags=[f'Node{y.__hash__()}', 'txt1'])
                    txt2_bg = view.canvas_now.create_rectangle(view.canvas_now.bbox(txt2), fill='white',
                                                               tags=['swap1', 'txt2'])
                    view.canvas_now.tag_lower(txt1_bg, txt1)
                    view.canvas_now.tag_lower(txt2_bg, txt2)
                    view.move_object('txt1', node.x, node.y, y.x, y.y)
                    view.move_object('txt2', y.x, y.y, node.x, node.y)
                    node.value = y.value
                    view.canvas_now.delete('swap1')
                    view.draw_node(node, view.canvas_now)
                view.move_object(f'Node{y.__hash__()}', y.x, y.y, y.x, - view.node_size)
                view.explanation.append(f'Remove {value} from tree')
                if y.color == 'black':
                    self.fix_delete(x)
                    view.animate_rotations(self.tree.root)
                    view.draw_recolor_text(x, 'black')
                    r.wait(view.animation_time)
                    view.canvas_now.delete('recolor_txt')
                view.explanation.append(f'Deletion finished')
                if type(self.tree.root) is RBTree.RBLeaf:
                    self.tree.clear()

        def fix_delete(self, node):
            """
            Fixes the red-black tree constraints in node subtree after the deletion process
            :node: node to start fixing process
            :return: returns nothing
            """
            view = self.tree.view
            while node is not self.tree.root and node.color == 'black':
                if node == node.parent.left:
                    w = node.parent.right
                    if type(w) is not RBTree.RBLeaf and w.color == 'red':
                        w.color = 'black'
                        node.parent.color = 'red'
                        tmp_node1, tmp_node2 = w, node.parent
                        node.parent.rotate('left')
                        view.draw_recolor_text(tmp_node1, 'black')
                        view.draw_recolor_text(tmp_node2, 'red')
                        r.wait(view.animation_time)
                        view.draw_node(tmp_node1, view.canvas_now)
                        view.draw_node(tmp_node2, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        w = node.parent.right
                    if type(w) is not RBTree.RBLeaf and w.left.color == 'black' and w.right.color == 'black':
                        w.color = 'red'
                        view.draw_recolor_text(w, 'red')
                        r.wait(view.animation_time)
                        view.draw_node(w, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        node = node.parent
                    elif type(w) is not RBTree.RBLeaf and w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        tmp_node1, tmp_node2 = w.left, w
                        w.rotate('right')
                        view.draw_recolor_text(tmp_node1, 'black')
                        view.draw_recolor_text(tmp_node2, 'red')
                        r.wait(view.animation_time)
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
                            node.parent.rotate('left')
                        view.draw_recolor_text(tmp_node1, node.parent.color)
                        view.draw_recolor_text(tmp_node2, 'black')
                        view.draw_recolor_text(tmp_node3, 'black')
                        r.wait(view.animation_time)
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
                        node.parent.rotate('right')
                        view.draw_recolor_text(tmp_node1, 'black')
                        view.draw_recolor_text(tmp_node2, 'red')
                        r.wait(view.animation_time)
                        view.draw_node(tmp_node1, view.canvas_now)
                        view.draw_node(tmp_node2, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        w = node.parent.left
                    if type(w) is not RBTree.RBLeaf and w.right.color == 'black' and w.left.color == 'black':
                        w.color = 'red'
                        view.draw_recolor_text(w, 'red')
                        r.wait(view.animation_time)
                        view.draw_node(w, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        node = node.parent
                    elif type(w) is not RBTree.RBLeaf and w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        tmp_node1, tmp_node2 = w.right, w
                        w.rotate('left')
                        view.draw_recolor_text(tmp_node1, 'black')
                        view.draw_recolor_text(tmp_node2, 'red')
                        r.wait(view.animation_time)
                        view.draw_node(tmp_node1, view.canvas_now)
                        view.draw_node(tmp_node2, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        w = node.parent.left
                    if node is not self.tree.root:
                        w.color = node.parent.color
                        node.parent.color = 'black'
                        w.left.color = 'black'
                        tmp_node1, tmp_node2, tmp_node3 = w, node.parent, w.left
                        if node.parent is not self.tree.root:
                            node.parent.rotate('right')
                        view.draw_recolor_text(tmp_node1, node.parent.color)
                        view.draw_recolor_text(tmp_node2, 'black')
                        view.draw_recolor_text(tmp_node3, 'black')
                        r.wait(view.animation_time)
                        view.draw_node(tmp_node1, view.canvas_now)
                        view.draw_node(tmp_node2, view.canvas_now)
                        view.draw_node(tmp_node3, view.canvas_now)
                        view.canvas_now.delete('recolor_txt')
                        node = self.tree.root
            node.color = 'black'

        def successor(self):
            """
            Finds the successor of the value in self node
            :return: successor node
            """
            view = self.tree.view
            if type(self.right) is not RBTree.RBLeaf:
                view.move_object('hint_frame', self.x, self.y, self.right.x, self.right.y)
                view.draw_exp_text(self.right, f'Looking for the minimum of {self.right.value}')
                tmp = self.right.subtree_minimum()
                return tmp
            y = self.parent
            while type(y) is not RBTree.RBLeaf and self is y.right:
                x = y
                y = x.parent
            view.explanation.append(f'{y.value}')
            return y

        def subtree_minimum(self):
            """
            Finds the node with minimal value in the given subtree starting in self
            :return: the node with minimal value
            """
            subtree = self
            view = self.tree.view
            while type(subtree.left) is not RBTree.RBLeaf:
                view.draw_exp_text(subtree, f'{subtree.value} has a left child ')
                view.move_object('hint_frame', subtree.x, subtree.y, subtree.left.x, subtree.left.y)
                subtree = subtree.left
            view.draw_exp_text(subtree, f'Minimum found: {subtree.value}')
            return subtree

        def search_value(self, value, show_to_gui=True):
            """
            Looks for the value in the tree. Shows the process in the GUI
            :param value: value to be found
            :param show_to_gui: if True labels will show info about search process
            :return: found node or None
            """
            view = self.tree.view
            view.explanation.append(f'Looking for a node {value}')
            curr = self.tree.root
            view.canvas_now.create_rectangle(curr.x - view.half_node_size,
                                             curr.y - view.half_node_size,
                                             curr.x + view.half_node_size,
                                             curr.y + view.half_node_size,
                                             outline='red', tags='hint_frame')
            while type(curr) is not RBTree.RBLeaf and curr.value != value:
                if curr.value > value and type(curr.left) is RBTree.RBNode:
                    view.draw_exp_text(curr, f'{value} < {curr.value}. Choosing left subtree')
                    view.move_object('hint_frame', curr.x, curr.y, curr.left.x, curr.left.y)
                    curr = curr.left
                elif curr.value > value:
                    view.draw_exp_text(curr, f'{value} < {curr.value}. Choosing left subtree')
                    unit = (curr.r_edge - curr.l_edge) / 4
                    view.move_object('hint_frame', curr.x, curr.y, curr.x - unit, curr.y + view.y_space)
                    view.draw_exp_text(
                        RBTree.RBNode(self.tree, curr.x - unit, curr.y + view.y_space, None, None, None, None),
                        'Element not found')
                    view.canvas_now.delete('hint_frame')
                    return None
                elif curr.value <= value and type(curr.right) is RBTree.RBNode:
                    view.draw_exp_text(curr, f'{value} >= {curr.value}. Choosing right subtree')
                    view.move_object('hint_frame', curr.x, curr.y, curr.right.x, curr.right.y)
                    curr = curr.right
                elif curr.value <= value:
                    view.draw_exp_text(curr, f'{value} >= {curr.value}. Choosing right subtree')
                    unit = (curr.r_edge - curr.l_edge) / 4
                    view.move_object('hint_frame', curr.x, curr.y, curr.x + unit, curr.y + view.y_space)
                    view.draw_exp_text(
                        RBTree.RBNode(self.tree, curr.x + unit, curr.y + view.y_space, None, None, None, None),
                        'Element not found')
                    view.canvas_now.delete('hint_frame')
                    return None
            view.draw_exp_text(curr, f'{curr.value} found')
            if show_to_gui:
                view.info_label.config(
                    text=f'Elem \'{value}\' found' if type(
                        curr) is not RBTree.RBLeaf else f'Elem \'{value}\' not found')
                view.canvas_now.delete('hint_frame')
            else:
                return curr

        def search_value_no_GUI(self, value):
            """
            Looks for the value in the subtree without the use of GUI
            :param value: value to be found
            :return: node with the value or None
            """
            curr = self.tree.root
            while type(curr) is RBTree.RBNode and curr.value != value:
                if curr.value > value and type(curr.left) is RBTree.RBNode:
                    curr = curr.left
                elif curr.value > value:
                    return None
                elif curr.value <= value and type(curr.right) is RBTree.RBNode:
                    curr = curr.right
                elif curr.value <= value:
                    return None
            return curr

        def print_node(self, i=0):
            """
            Prints the node to the terminal
            :param i: indent - equivalent to the height on which the node lies in the tree
            :return: returns nothing
            """
            print(' ' * i + f'{self.value}')
            i += 1
            self.left.print_node(i)
            self.right.print_node(i)
            i -= 1
