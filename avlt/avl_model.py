import core.root as r
import mvc_base.model as model

left = 'left'
right = 'right'


class AVLTree(model.Tree):

    def insert_value(self, value):
        if self.root is None:
            self.root = AVLTNode(value, self.view.width // 2, self.view.y_space, self, 0, self.view.width)
            self.view.explanation.append(f'Tree is empty')
            self.view.explanation.append(f'Added node {value}')
        else:
            self.root.insert_value(value)
            self.view.draw_exp_text(self.root, f'Calculate height')

    def delete_value(self, value):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to delete form empty tree')
        else:
            self.root.delete_value(value)
            self.view.draw_exp_text(self.root, f'Calculate height')

    def search_value(self, value):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Value cannot be found')
        else:
            self.root.search_value(value)

    def search_value_no_GUI(self, value):
        if self.root is not None:
            return self.root.search_value_no_GUI(value)

    def clear(self):
        self.root = None


class AVLTLeaf:
    left = None
    right = None

    def __init__(self):
        pass

    def update_positions(self, static=None):
        pass

    @staticmethod
    def successors():
        return []

    def print_node(self, i):
        pass

    @staticmethod
    def get_height():
        return 0

    @staticmethod
    def get_balance():
        return 0


class AVLTNode(model.AnimatedObject, model.Node):
    def __init__(self, value, x, y, tree, l_edge=None, r_edge=None, parent=None):
        model.AnimatedObject.__init__(self, x, y, parent)
        model.Node.__init__(self, tree, l_edge, r_edge)
        self.value = value
        self.left = AVLTLeaf()
        self.right = AVLTLeaf()
        self.height = 1

    def tick(self, view, x_unit, y_unit):
        view.erase(f'Line{hash(self)}')
        view.erase(f'Line{hash(self.parent)}')
        view.canvas_now.move(self.tag(), x_unit, y_unit)
        self.x += x_unit
        self.y += y_unit
        view.draw_line(view.canvas_now, self, self.right)
        view.draw_line(view.canvas_now, self, self.left)
        # Drawing self-self.parent line
        if type(self.parent) is AVLTNode and self.parent.right is self:
            view.draw_line(view.canvas_now, self.parent, self.parent.right)
        elif type(self.parent) is AVLTNode and self.parent.left is self:
            view.draw_line(view.canvas_now, self.parent, self.parent.left)
        view.canvas_now.tag_lower('Line')

    def tag(self):
        return f'Node{hash(self)}'

    def insert_value(self, value):
        """
        Inserts value into the node
        :param value: value to insert
        :return: returns nothing
        """
        view = self.tree.view
        root = self.tree.root
        view.explanation.append(f'Tree is not empty, looking for insert place for {value}')
        view.canvas_now.create_oval(root.x - view.node_width // 2, root.y - view.y_above - view.node_height // 2,
                                    root.x + view.node_width // 2, root.y - view.y_above + view.node_height // 2,
                                    fill='grey', tags=r.grey_node)
        view.canvas_now.create_text(root.x, root.y - view.y_above, fill='white', text=value, tags=r.grey_node)
        newNode = root.subtree_insert_value(value)
        view.draw_exp_text(newNode, f'Inserting {newNode.value}', False)
        view.explanation.append(f'{value} inserted. Starting fixing')
        view.draw_object_with_children_lines(newNode, view.canvas_now)
        view.erase(r.grey_node)
        view.draw_line(view.canvas_now, newNode, newNode.parent)
        view.canvas_now.tag_lower(f'Line{hash(newNode)}')
        newNode.fix_insert(value)

    def delete_value(self, value):
        """
        Deletes the value from the node or subnodes
        :param value: value to be deleted
        :return: returns nothing
        """
        view = self.tree.view
        node = self.search_value(value, False)
        if type(node) is not AVLTNode:
            view.info_label.config(text=f'There is no element \'{value}\' in the tree')
            return
        else:
            # Delete from tree with only root node
            if node is self.tree.root and type(node.left) is AVLTLeaf and type(node.right) is AVLTLeaf:
                view.erase(r.hint_frame)
                view.move_object(self.tree.root.tag(), self.tree.root.x, self.tree.root.y, self.tree.root.x,
                                 -view.node_width)
                self.tree.clear()
                return
            if type(node.left) is AVLTLeaf or type(node.right) is AVLTLeaf:
                view.explanation.append(f'Right or left child of {node.value} is a leaf')
                y = node
            else:
                view.draw_exp_text(node, f'Looking for the successor of {node.value}')
                y = node.successor()
            if type(y.left) is not AVLTLeaf:
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
            view.erase(f'Line{hash(y)}')
            view.erase(r.hint_frame)
            self.tree.root.update_positions()
            if y is not node:
                view.explanation.append(f'Swap {node.value} with {y.value}')
                view.canvas_now.create_oval(node.x - view.node_width // 2, node.y - view.node_height // 2,
                                            node.x + view.node_width // 2, node.y + view.node_height // 2,
                                            fill='green', tags='swap1')
                view.canvas_now.create_oval(y.x - view.node_width // 2, y.y - view.node_height // 2,
                                            y.x + view.node_width // 2, y.y + view.node_height // 2,
                                            fill='green', tags=y.tag())
                txt1 = view.canvas_now.create_text(node.x, node.y, fill='blue', text=node.value, tags=[y.tag(), 'txt1'])
                txt2 = view.canvas_now.create_text(y.x, y.y, fill='blue', text=y.value, tags=['swap1', 'txt2'])
                txt1_bg = view.canvas_now.create_rectangle(view.canvas_now.bbox(txt1), fill='white',
                                                           tags=[y.tag(), 'txt1'])
                txt2_bg = view.canvas_now.create_rectangle(view.canvas_now.bbox(txt2), fill='white',
                                                           tags=['swap1', 'txt2'])
                view.canvas_now.tag_lower(txt1_bg, txt1)
                view.canvas_now.tag_lower(txt2_bg, txt2)
                view.move_object('txt1', node.x, node.y, y.x, y.y)
                view.move_object('txt2', y.x, y.y, node.x, node.y)
                node.value = y.value
                view.erase('swap1')
                view.draw_object(node, view.canvas_now)
            view.move_object(y.tag(), y.x, y.y, y.x, - view.node_height)
            view.explanation.append(f'Remove {value} from tree')
            self.fix_delete()
            view.animate(self.tree.root)
            view.explanation.append(f'Deletion finished')
            if type(self.tree.root) is AVLTLeaf:
                self.tree.clear()

    def search_value(self, value, show_to_gui=True):
        """
        Searches for the value in the tree. Shows the process in the GUI
        :param value: value to be found
        :param show_to_gui: if True labels will show info about search process
        :return: found node or None
        """
        view = self.tree.view
        view.explanation.append(f'Looking for a node {value}')
        curr = self.tree.root
        view.hint_frame.draw(curr.x, curr.y)
        while type(curr) is not AVLTLeaf and curr.value != value:
            if curr.value > value and type(curr.left) is AVLTNode:
                view.draw_exp_text(curr, f'{value} < {curr.value}. Choosing left subtree')
                view.hint_frame.move(curr.left.x, curr.left.y)
                curr = curr.left
            elif curr.value > value:
                view.draw_exp_text(curr, f'{value} < {curr.value}. Choosing left subtree')
                unit = (curr.r_edge - curr.l_edge) / 4
                view.hint_frame.move(curr.x - unit, curr.y + view.y_space)
                view.draw_exp_text(AVLTNode(None, curr.x - unit, curr.y + view.y_space, self.tree), 'Element not found')
                view.erase(r.hint_frame)
                return None
            elif curr.value <= value and type(curr.right) is AVLTNode:
                view.draw_exp_text(curr, f'{value} >= {curr.value}. Choosing right subtree')
                view.hint_frame.move(curr.right.x, curr.right.y)
                curr = curr.right
            elif curr.value <= value:
                view.draw_exp_text(curr, f'{value} >= {curr.value}. Choosing right subtree')
                unit = (curr.r_edge - curr.l_edge) / 4
                view.hint_frame.move(curr.x + unit, curr.y + view.y_space)
                view.draw_exp_text(AVLTNode(None, curr.x + unit, curr.y + view.y_space, self.tree), 'Element not found')
                view.erase(r.hint_frame)
                return None
        view.draw_exp_text(curr, f'{curr.value} found')
        if show_to_gui:
            view.info_label.config(
                text=f'Elem \'{value}\' found' if type(curr) is not AVLTLeaf else f'Elem \'{value}\' not found')
            view.erase(r.hint_frame)
        else:
            return curr

    def search_value_no_GUI(self, value):
        """
        Searches for the value in the subtree without the use of GUI
        :param value: value to be found
        :return: node with the value or None
        """
        curr = self.tree.root
        while type(curr) is AVLTNode and curr.value != value:
            if curr.value > value and type(curr.left) is AVLTNode:
                curr = curr.left
            elif curr.value > value:
                return None
            elif curr.value <= value and type(curr.right) is AVLTNode:
                curr = curr.right
            elif curr.value <= value:
                return None
        return curr

    def update_positions(self, static=False, width=None):
        view = self.tree.view
        if type(self.parent) is AVLTNode:
            self.parent: AVLTNode
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

    def successors(self):
        result = []
        result += self.left.successors()
        result += self.right.successors()
        result.append(self)
        return result

    def successor(self):
        """
        Finds the successor of the value in self node
        :return: successor node
        """
        view = self.tree.view
        # successor is below the node
        if type(self.right) is AVLTNode:
            self.right: AVLTNode
            view.hint_frame.move(self.right.x, self.right.y)
            view.draw_exp_text(self.right, f'Looking for the minimum of {self.right.value}')
            minimum = self.right.subtree_minimum()
            return minimum
        # successor is above the node
        else:
            parent = self.parent
            while type(parent) is AVLTNode and self is parent.right:
                current = parent
                parent = current.parent
            if type(parent) is AVLTNode:
                view.explanation.append(f'{parent.value}')
            return parent

    def print_node(self, indent=0):
        print(' ' * indent + f'{self.value}')
        indent += 1
        self.left.print_node(indent)
        self.right.print_node(indent)
        indent -= 1

    # AVLNode specific methods below

    def subtree_insert_value(self, value):
        """
        Looks for the place to insert a new value
        :param value: value to be inserted
        :return: reference to the inserted node
        """
        view = self.tree.view
        unit = (self.r_edge - self.l_edge) / 4
        if value >= self.value and type(self.right) is AVLTNode:
            view.draw_exp_text(self, f'{value} >= {self.value} --> choosing right subtree', False)
            view.move_object(r.grey_node, self.x, self.y - view.node_height // 2 - view.y_above, self.right.x,
                             self.right.y - view.node_height // 2 - view.y_above)
            newNode = self.right.subtree_insert_value(value)
        elif value >= self.value:
            view.draw_exp_text(self, f'{value} >= {self.value} --> choosing right subtree', False)
            newNode = AVLTNode(value, self.x + unit, self.y + view.y_space, self.tree, self.x, self.r_edge, self)
            self.right = newNode
            view.move_object(r.grey_node, self.x, self.y - view.node_height // 2 - view.y_above, self.right.x,
                             self.right.y - view.node_height // 2)
        elif value < self.value and type(self.left) is AVLTNode:
            view.draw_exp_text(self, f'{value} < {self.value} --> choosing left subtree', False)
            view.move_object(r.grey_node, self.x, self.y - view.node_height // 2 - view.y_above, self.left.x,
                             self.left.y - view.node_height // 2 - view.y_above)
            newNode = self.left.subtree_insert_value(value)
        else:
            view.draw_exp_text(self, f'{value} < {self.value} --> choosing left subtree', False)
            newNode = AVLTNode(value, self.x - unit, self.y + view.y_space, self.tree, self.l_edge, self.x, self)
            self.left = newNode
            view.move_object(r.grey_node, self.x, self.y - view.node_height // 2 - view.y_above, self.left.x,
                             self.left.y - view.node_height // 2)
        self.height = 1 + max(self.left.get_height(), self.right.get_height())
        return newNode

    def fix_insert(self, value):
        """
        Fixes the AVL subtree after the insertion process. Starts in self
        :param value: value that was inserted
        :return: returns nothing
        """
        self.height = 1 + max(self.left.get_height(), self.right.get_height())
        balance = self.get_balance()
        if balance > 1 and type(self.left) is AVLTNode and value < self.left.value:
            self.rotate(right)
        if balance < -1 and type(self.right) is AVLTNode and value > self.right.value:
            self.rotate(left)
        if balance > 1 and type(self.left) is AVLTNode and value > self.left.value:
            self.left.rotate(left)
            self.rotate(right)
        if balance < -1 and type(self.right) is AVLTNode and value < self.right.value:
            self.right.rotate(right)
            self.rotate(left)
        if self.parent is not None:
            self.parent.fix_insert(value)

    def fix_delete(self):
        """
        Fixes the AVL tree constraints in node subtree after the deletion process
        :node: node to start fixing process
        :return: returns nothing
        """
        self.height = 1 + max(self.left.get_height(), self.right.get_height())
        balance = self.get_balance()
        if balance > 1 and type(self.left) is AVLTNode and self.left.get_balance() >= 0:
            self.rotate(right)
        if balance < -1 and type(self.right) is AVLTNode and self.right.get_balance() <= 0:
            self.rotate(left)
        if balance > 1 and type(self.left) is AVLTNode and self.left.get_balance() < 0:
            self.left.rotate(left)
            self.rotate(right)
        if balance < -1 and type(self.right) is AVLTNode and self.right.get_balance() > 0:
            self.right.rotate(right)
            self.rotate(left)
        if self.parent is not None:
            self.parent.fix_delete()

    def rotate(self, side):
        """
        Performs the left or right rotation operation
        :param side: string: 'left' or 'right'
        :return: returns node which is now the root of subtree
        """
        view = self.tree.view
        view.draw_exp_text(self, f'{side}-rotate on {self.value}')
        y = self[right if side == left else left]
        self[right if side == left else left] = y[side]
        if type(y[side]) is not AVLTLeaf:
            y[side].parent = self
        y.parent = self.parent
        if self.parent is None:
            self.tree.root = y
        elif self == self.parent[side]:
            self.parent[side] = y
        else:
            self.parent[right if side == left else left] = y
        y[side] = self
        self.parent = y
        self.height = 1 + max(self.left.get_height(), self.right.get_height())
        y.height = 1 + max(y.left.get_height(), y.right.get_height())
        self.tree.root.update_positions()
        view.animate(y)
        return y

    def subtree_minimum(self):
        """
        Finds the node with minimal value in the given subtree starting in self
        :return: the node with minimal value
        """
        subtree = self
        view = self.tree.view
        while type(subtree.left) is not AVLTLeaf:
            view.draw_exp_text(subtree, f'{subtree.value} has a left child ')
            view.hint_frame.move(subtree.left.x, subtree.left.y)
            subtree = subtree.left
        view.draw_exp_text(subtree, f'Minimum found: {subtree.value}')
        return subtree

    def __getitem__(self, item):
        """
        Enables to get self.left with self['left'] and self.right with self['right']
        :param item: string: 'left' or 'right'
        :return: self.left or self.right
        """
        if item == left:
            return self.left
        elif item == right:
            return self.right

    def __setitem__(self, key, value):
        """
        Enables to set self.left with self['left']=value and self.right with self['right']=value
        :param key: string: 'left' or 'right'
        :param value: new value of the attribute
        :return: returns nothing
        """
        if key == left:
            self.left = value
        elif key == right:
            self.right = value

    def get_height(self):
        return self.height

    def get_balance(self):
        return self.left.get_height() - self.right.get_height()
