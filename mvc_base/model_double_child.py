# Contains base classes for model components with maximum of two child nodes - Double Child
import abc
import statistics

from PIL import ImageTk, Image

import mvc_base.model as model
from core.constants import left, right, white, black, grey_node, hint_frame


class DCTree(model.Tree, abc.ABC):
    """Contains methods similar in all Double Child trees"""

    def __init__(self, view):
        super().__init__(view)
        grey_circle = Image.open('../materials/grey_circle.png').resize((self.view.node_width, self.view.node_height),
                                                                        Image.ANTIALIAS)
        self.grey_circle = ImageTk.PhotoImage(grey_circle)

    # Tree derived methods override

    def delete_value(self, value):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to delete from an empty tree')
        else:
            self.root.delete_value(value)

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

    def min(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate min of an empty tree')
        else:
            self.root.min()

    def max(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate max of an empty tree')
        else:
            self.root.max()

    def mean(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate mean of an empty tree')
        else:
            self.view.explanation.append(f'Calculate the mean value of the tree - traverse tree in order')
            self.view.hint_frame.draw(self.root.x, self.root.y)
            val_sum, counter = self.root.mean(0, 0)
            self.view.draw_exp_text(self.root, f'Whole tree traversed. '
                                               f'Mean = {val_sum}/{counter} = {val_sum / counter}')

    def median(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate median of an empty tree')
        else:
            self.view.explanation.append(f'Calculate the median of the tree - traverse tree in order')
            self.view.hint_frame.draw(self.root.x, self.root.y)
            tab = self.root.median([])
            self.view.draw_exp_text(self.root,
                                    f'Whole tree traversed. Values = {tab}. Median = {statistics.median(tab)}')

    # DCTree specific methods

    def insert_value_helper(self, value):
        view = self.view
        root = self.root
        view.explanation.append(f'Tree is not empty. Find insert place for {value}')
        view.canvas_now.create_image(root.x - view.node_width // 2, root.y - view.y_above - view.node_height // 2,
                                     anchor='nw', image=self.grey_circle, tags=grey_node)
        view.canvas_now.create_text(root.x, root.y - view.y_above, fill=white, text=value, tags=grey_node)
        newNode = root.insert_value(value)
        view.explanation.append(f'Start node-fixing process')
        view.draw_object_with_children_lines(newNode, view.canvas_now)
        view.erase(grey_node)
        view.draw_line(view.canvas_now, newNode, newNode.parent)
        view.canvas_now.tag_lower(f'Line{hash(newNode)}')
        newNode.fix_insert(value)
        self.view.explanation.append(f'Fixing nodes finished')


class DCLeaf:
    """Universal Leaf class for both RBT-leaves and AVL-leaves"""
    color = black  # For RB Tree
    height = 0  # For AVL Tree
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
    def get_balance():
        return 0

    def median(self, tab):
        pass

    def mean(self, val_sum, counter):
        pass


class DCNode(model.AnimatedObject, model.Node):

    def __init__(self, value, x, y, tree, l_edge=None, r_edge=None, parent=None):
        model.AnimatedObject.__init__(self, x, y, parent)
        model.Node.__init__(self, tree, l_edge, r_edge)
        self.value = value
        self.left = DCLeaf()
        self.right = DCLeaf()

    # Node derived methods override

    def tick(self, view, x_unit, y_unit):
        view.erase(f'Line{hash(self)}')
        view.erase(f'Line{hash(self.parent)}')
        view.canvas_now.move(self.tag(), x_unit, y_unit)
        self.x += x_unit
        self.y += y_unit
        view.draw_line(view.canvas_now, self, self.right)
        view.draw_line(view.canvas_now, self, self.left)
        # Drawing self.parent-self and self.parent-sibling(self) lines
        if type(self.parent) is self.tree.node_class:
            view.draw_line(view.canvas_now, self.parent, self.parent.right)
            view.draw_line(view.canvas_now, self.parent, self.parent.left)

    def tag(self):
        return f'Node{hash(self)}'

    def insert_value(self, value):
        """
        Looks for the place to insert a new value
        :param value: value to be inserted
        :return: reference to the inserted node
        """
        view = self.tree.view
        unit = (self.r_edge - self.l_edge) / 4
        klass = self.tree.node_class
        # Insert into appropriate subtree
        if value >= self.value and type(self.right) is klass:
            view.draw_exp_text(self, f'{value} >= {self.value}, so insert into right subtree', False)
            view.move_object(grey_node, self.x, self.y - view.node_height // 2 - view.y_above, self.right.x,
                             self.right.y - view.node_height // 2 - view.y_above)
            newNode = super(klass, self.right).insert_value(value)
        # self.right is not a Node subclass
        elif value >= self.value:
            view.draw_exp_text(self, f'{value} >= {self.value}, so insert into right subtree', False)
            newNode = klass(value, self.x + unit, self.y + view.y_space, self.tree, self.x, self.r_edge, self)
            self.right = newNode
            view.move_object(grey_node, self.x, self.y - view.node_height // 2 - view.y_above, self.right.x,
                             self.right.y - view.node_height // 2)
        elif value < self.value and type(self.left) is klass:
            view.draw_exp_text(self, f'{value} < {self.value}, so insert into left subtree', False)
            view.move_object(grey_node, self.x, self.y - view.node_height // 2 - view.y_above, self.left.x,
                             self.left.y - view.node_height // 2 - view.y_above)
            newNode = super(klass, self.left).insert_value(value)
        # self.left is not a Node subclass
        else:
            view.draw_exp_text(self, f'{value} < {self.value}, so insert into left subtree', False)
            newNode = klass(value, self.x - unit, self.y + view.y_space, self.tree, self.l_edge, self.x, self)
            self.left = newNode
            view.move_object(grey_node, self.x, self.y - view.node_height // 2 - view.y_above, self.left.x,
                             self.left.y - view.node_height // 2)
        return newNode

    def delete_value(self, value):
        """
        Deletes the value from the node or subnodes
        :param value: value to be deleted
        :return: returns tuple (x,y) of nodes # TODO
        """
        view = self.tree.view
        node = self.search_value(value)
        if node is None:
            return None, None
        # Delete from tree with only root node
        if node is self.tree.root and type(node.left) is DCLeaf and type(node.right) is DCLeaf:
            view.erase(hint_frame)
            view.move_object(self.tree.root.tag(), self.tree.root.x, self.tree.root.y, self.tree.root.x,
                             -view.node_height)
            self.tree.clear()
            return None, None
        if type(node.left) is DCLeaf or type(node.right) is DCLeaf:
            view.explanation.append(f'Right or left child of ({node.value}) is a leaf')
            y = node
        else:
            view.draw_exp_text(node, f'Find the successor of ({node.value})')
            y = node.successor()
        if type(y.left) is not DCLeaf:
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
        view.erase(hint_frame)
        self.tree.root.update_positions()
        # Swap values in two nodes: one holding value to delete and it's successor
        if y is not node:
            view.explanation.append(f'Swap {node.value} with {y.value}')
            circle_node = view.black_circle if node.color == black else view.red_circle
            circle_y = view.black_circle if y.color == black else view.red_circle
            view.canvas_now.create_image(node.x - view.node_width // 2, node.y - view.node_height // 2,
                                         image=circle_node, anchor='nw', tags='swap1')
            view.canvas_now.create_image(y.x - view.node_width // 2, y.y - view.node_height // 2,
                                         image=circle_y, anchor='nw', tags=y.tag())
            txt1 = view.canvas_now.create_text(node.x, node.y, fill=black, text=node.value, tags=[y.tag(), 'txt1'])
            txt2 = view.canvas_now.create_text(y.x, y.y, fill=black, text=y.value, tags=['swap1', 'txt2'])
            txt1_bg = view.canvas_now.create_rectangle(view.canvas_now.bbox(txt1), fill=white, tags=[y.tag(), 'txt1'])
            txt2_bg = view.canvas_now.create_rectangle(view.canvas_now.bbox(txt2), fill=white, tags=['swap1', 'txt2'])
            view.canvas_now.tag_lower(txt1_bg, txt1)
            view.canvas_now.tag_lower(txt2_bg, txt2)
            view.move_object('txt1', node.x, node.y, y.x, y.y)
            view.move_object('txt2', y.x, y.y, node.x, node.y)
            node.value = y.value
            view.erase('swap1')
            view.draw_object(node, view.canvas_now)
        view.move_object(y.tag(), y.x, y.y, y.x, - view.node_height)
        view.explanation.append(f'Remove {value} from tree')
        return x, y

    def search_value(self, value):
        """
        Searches for the value in the tree. Shows the process in the GUI
        :param value: value to be found
        :return: found node or None
        """
        view = self.tree.view
        view.explanation.append(f'Search for a node with value {value}')
        curr = self.tree.root
        klass = self.tree.node_class
        view.hint_frame.draw(curr.x, curr.y)
        while type(curr) is not DCLeaf and curr.value != value:
            if curr.value > value and type(curr.left) is klass:
                view.draw_exp_text(curr, f'{value} < {curr.value}, so search in left subtree')
                view.hint_frame.move(curr.left.x, curr.left.y)
                curr = curr.left
            elif curr.value > value:
                view.draw_exp_text(curr, f'{value} < {curr.value}, so search in left subtree')
                unit = (curr.r_edge - curr.l_edge) / 4
                view.hint_frame.move(curr.x - unit, curr.y + view.y_space)
                view.draw_exp_text(klass(None, curr.x - unit, curr.y + view.y_space, self.tree), 'Element not found')
                view.erase(hint_frame)
                return None
            elif curr.value <= value and type(curr.right) is klass:
                view.draw_exp_text(curr, f'{value} >= {curr.value}, so search in right subtree')
                view.hint_frame.move(curr.right.x, curr.right.y)
                curr = curr.right
            elif curr.value <= value:
                view.draw_exp_text(curr, f'{value} >= {curr.value}, so search in right subtree')
                unit = (curr.r_edge - curr.l_edge) / 4
                view.hint_frame.move(curr.x + unit, curr.y + view.y_space)
                view.draw_exp_text(klass(None, curr.x + unit, curr.y + view.y_space, self.tree), 'Element not found')
                view.erase(hint_frame)
                return None
        view.draw_exp_text(curr, f'Node ({curr.value}) found')
        return curr

    def search_value_no_GUI(self, value):
        """
        Searches for the value in the subtree without the use of GUI
        :param value: value to be found
        :return: node with the value or None, None
        """
        curr = self.tree.root
        klass = self.tree.node_class
        while type(curr) is klass and curr.value != value:
            if curr.value > value and type(curr.left) is klass:
                curr = curr.left
            elif curr.value > value:
                return None, None
            elif curr.value <= value and type(curr.right) is klass:
                curr = curr.right
            elif curr.value <= value:
                return None, None
        return curr

    def update_positions(self, static=False, width=None):
        view = self.tree.view
        klass = self.tree.node_class
        if type(self.parent) is klass:
            self.parent: DCNode
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
        klass = self.tree.node_class
        # successor is below the node
        if type(self.right) is klass:
            self.right: DCNode
            view.hint_frame.move(self.right.x, self.right.y)
            view.draw_exp_text(self.right, f'Find the minimum of ({self.right.value}) subtree')
            minimum = self.right.subtree_minimum()
            return minimum
        # successor is above the node
        else:
            parent = self.parent
            while type(parent) is klass and self is parent.right:
                current = parent
                parent = current.parent
            if type(parent) is klass:
                view.explanation.append(f'{parent.value}')
            return parent

    def print_node(self, indent=0):
        print(' ' * indent + f'{self.value}')
        indent += 1
        self.left.print_node(indent)
        self.right.print_node(indent)
        indent -= 1

    def min(self):
        view = self.tree.view
        view.explanation.append(f'Search the minimal value of the tree')
        curr = self.tree.root
        view.hint_frame.draw(curr.x, curr.y)
        while type(curr.left) is not DCLeaf:
            view.draw_exp_text(curr, f'Node [{curr.value}] has left child. Search from min there')
            view.hint_frame.move(curr.left.x, curr.left.y)
            curr = curr.left
        view.draw_exp_text(curr, f'Node [{curr.value}] has no left child. It\'s the min value of the tree')

    def max(self):
        view = self.tree.view
        view.explanation.append(f'Search the maximal value of the tree')
        curr = self.tree.root
        view.hint_frame.draw(curr.x, curr.y)
        while type(curr.right) is not DCLeaf:
            view.draw_exp_text(curr, f'Node [{curr.value}] has right child. Search from max there')
            view.hint_frame.move(curr.right.x, curr.right.y)
            curr = curr.right
        view.draw_exp_text(curr, f'Node [{curr.value}] has no right child. It\'s the max value of the tree')

    def mean(self, val_sum, counter):
        view = self.tree.view
        if type(self.left) is not DCLeaf:
            self.left: DCNode
            view.draw_exp_text(self, f'Go to left child of node [{self.value}]')
            view.hint_frame.move(self.left.x, self.left.y)
            val_sum, counter = self.left.mean(val_sum, counter)
            view.draw_exp_text(self, f'Go to parent node [{self.value}]')
            view.hint_frame.move(self.x, self.y)
        view.draw_exp_text(self, f'Add {self.value} to sum {val_sum} and increase counter {counter} by 1')
        val_sum += self.value
        counter += 1
        if type(self.right) is not DCLeaf:
            self.right: DCNode
            view.draw_exp_text(self, f'Go to right child of node [{self.value}]')
            view.hint_frame.move(self.right.x, self.right.y)
            val_sum, counter = self.right.mean(val_sum, counter)
            view.draw_exp_text(self, f'Go to parent node [{self.value}]')
            view.hint_frame.move(self.x, self.y)
        return val_sum, counter

    def median(self, tab):
        view = self.tree.view
        if type(self.left) is not DCLeaf:
            self.left: DCNode
            view.draw_exp_text(self, f'Go to left child of node [{self.value}]')
            view.hint_frame.move(self.left.x, self.left.y)
            tab = (self.left.median(tab))
            view.draw_exp_text(self, f'Go to parent node [{self.value}]')
            view.hint_frame.move(self.x, self.y)
        view.draw_exp_text(self, f'Append {self.value} to tab {tab}')
        tab.append(self.value)
        if type(self.right) is not DCLeaf:
            self.right: DCNode
            view.draw_exp_text(self, f'Go to right child of node [{self.value}]')
            view.hint_frame.move(self.right.x, self.right.y)
            tab = (self.right.median(tab))
            view.draw_exp_text(self, f'Go to parent node [{self.value}]')
            view.hint_frame.move(self.x, self.y)
        return tab

    # DCNode specific methods

    def rotate(self, side):
        """
        Performs the left or right rotation operation
        :param side: string: 'left' or 'right'
        :return: returns node which is now the root of subtree
        """
        view = self.tree.view
        view.draw_exp_text(self, f'{side[0].upper() + side[1:]}-rotate on ({self.value}) node')
        y = self[right if side == left else left]
        self[right if side == left else left] = y[side]
        if type(y[side]) is not DCLeaf:
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
        return y

    def subtree_minimum(self):
        """
        Finds the node with minimal value in the given subtree starting in self
        :return: the node with minimal value
        """
        subtree = self
        view = self.tree.view
        while type(subtree.left) is not DCLeaf:
            view.draw_exp_text(subtree, f'Check ({subtree.value}) node left child ')
            view.hint_frame.move(subtree.left.x, subtree.left.y)
            subtree = subtree.left
        view.draw_exp_text(subtree, f'Minimum value found: {subtree.value}')
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

    @abc.abstractmethod
    def fix_insert(self, value=None):
        pass

    @abc.abstractmethod
    def fix_delete(self):
        pass
