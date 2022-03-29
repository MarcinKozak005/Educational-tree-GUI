import abc
import tkinter as tk

import mvc_base.model as model
from core.constants import grey_node, white, hint_frame


class MCTree(model.Tree):
    @property
    @abc.abstractmethod
    def node_class(self):
        pass

    @property
    @abc.abstractmethod
    def value_class(self):
        pass

    def __init__(self, view, max_degree):
        super().__init__(view)
        if max_degree < 2:
            raise ValueError
        self.max_degree = max_degree

    def insert_value(self, value):
        if self.root is None:
            self.root = self.node_class(self, True, self.view.width // 2, self.view.y_space)
            self.view.explanation.append(f'Tree is empty. Create node [{self.root.id}] with value {value}')
            self.root.values.append(self.value_class(value, self.root))
        else:
            view = self.view
            view.explanation.append(f'Tree is not empty. Find insert place for {value}')
            view.canvas_now.create_rectangle(self.root.x - view.node_width // 2,
                                             self.root.y - view.node_height // 2 - view.y_above,
                                             self.root.x + view.node_width // 2,
                                             self.root.y + view.node_height // 2 - view.y_above,
                                             fill='grey', tags=grey_node)
            view.canvas_now.create_text(self.root.x, self.root.y - view.y_above, fill=white,
                                        text=value, tags=grey_node)
            self.root.insert_value(self.value_class(value, None, self.root.x, self.root.y - view.y_above))
        self.root.update_positions(True)

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
        """ Additionally resets self.node_class.class_node_id """
        self.root = None
        self.node_class.class_node_id = ord('@')

    @abc.abstractmethod
    def min(self):
        pass

    @abc.abstractmethod
    def max(self):
        pass

    @abc.abstractmethod
    def mean(self):
        pass

    @abc.abstractmethod
    def median(self):
        pass


class MCValue(model.AnimatedObject):

    def __init__(self, value, parent_node, x=0, y=0):
        super().__init__(x, y, parent_node)
        self.value = value

    def tick(self, view, x_unit, y_unit):
        view.erase(f'Line{hash(self)}')
        if view.canvas_now.find_withtag(self.tag()):
            view.canvas_now.move(self.tag(), x_unit, y_unit)
        else:
            view.canvas_now.move(grey_node, x_unit, y_unit)
        self.x += x_unit
        self.y += y_unit
        index = self.parent.values.index(self)
        if not self.parent.is_leaf:
            if index < len(self.parent.children):
                view.draw_line(view.canvas_now, self, self.parent.children[index], tk.SW, tk.N)
            if index == len(self.parent.values) - 1 and index + 1 < len(self.parent.children):
                view.draw_line(view.canvas_now, self, self.parent.children[index + 1], tk.SE, tk.N)
            view.canvas_now.tag_lower('Line')

    def tag(self):
        return f'Value{hash(self)}'


class MCNode(model.AnimatedObject, model.Node, abc.ABC):
    @classmethod
    def get_id(cls):
        cls.class_node_id += 1
        if cls.class_node_id == ord('['):
            cls.class_node_id = ord('a')
        elif cls.class_node_id == ord('{'):
            cls.class_node_id = ord('A')
        return chr(cls.class_node_id)

    def __init__(self, tree, is_leaf, x, y):
        model.AnimatedObject.__init__(self, x, y, None)
        model.Node.__init__(self, tree, 0, tree.view.width)
        self.is_leaf = is_leaf
        self.values = []
        self.children = []
        self.id = type(self).get_id()

    def tick(self, view, x_unit, y_unit):
        view.canvas_now.move(self.tag(), x_unit, y_unit)
        self.x += x_unit
        self.y += y_unit

    def tag(self):
        return f'Node{hash(self)}'

    def search_value_no_GUI(self, value):
        """
        Searches for value in the node
        :param value: searched value
        :return: if found: tuple (node_with_value, position_of_value_in_node), else: None
        """
        i = 0
        while i < len(self.values) and value > self.values[i].value:
            i += 1
        if i < len(self.values) and value == self.values[i].value:
            return self, i
        if self.is_leaf:
            return None
        else:
            return self.children[i].search_value_no_GUI(value)

    def update_positions(self, static=False, width=None):
        view = self.tree.view
        if self.parent is not None:
            unit = (self.parent.r_edge - self.parent.l_edge) / (2 * len(self.parent.children))
            index = self.parent.children.index(self)
            self.x_next = self.parent.l_edge + unit + index * 2 * unit
            self.y_next = self.parent.y_next + view.y_space
            self.l_edge = self.x_next - unit
            self.r_edge = self.x_next + unit
        elif self.parent is None:
            self.x_next = view.width // 2 if width is None else width // 2
            self.y_next = view.y_space
            self.l_edge = 0
            self.r_edge = view.width if width is None else width
        # Values
        for i in range(len(self.values)):
            self.values[i].x_next = self.x_next - len(self.values) * self.tree.view.node_width // 2 + \
                                    self.tree.view.node_width // 2 + i * self.tree.view.node_width
            self.values[i].y_next = self.y_next
        if static:
            self.x = self.x_next
            self.y = self.y_next
            for v in self.values:
                v.x = v.x_next
                v.y = v.y_next
        if not self.is_leaf:
            for c in self.children:
                c.update_positions(static)

    def successors(self):
        result = []
        for c in self.children:
            result += c.successors()
        result.append(self)
        result += self.values
        return result

    @abc.abstractmethod
    def min(self):
        pass

    @abc.abstractmethod
    def max(self):
        pass

    @abc.abstractmethod
    def mean(self):
        pass

    @abc.abstractmethod
    def median(self):
        pass

    def fix_insert(self):
        """
        Fixes the node to make it obey max_degree constraint of b-trees
        :return: returns nothing
        """
        if self.parent is not None:
            self.parent.split_child(self.parent.children.index(self), self)
        else:
            self.tree.view.draw_exp_text(self, f'Root has too much values. Create new root and split old one')
            s = self.tree.node_class(self.tree, False, self.tree.view.width // 2, self.tree.view.y_space)
            s.children.insert(0, self.tree.root)
            self.tree.root.parent = s
            self.tree.root = s
            s.split_child(0, s.children[0])

    def predecessor(self):
        """
        Searches for predecessor in the tree starting in self.
        Removes the predecessor!
        :return: predecessor, node from which predecessor was deleted
        """
        last = self.values[-1]
        view = self.tree.view
        view.hint_frame.draw(last.x, last.y)
        if self.is_leaf:
            view.draw_exp_text(self, f'Node [{self.id}] is a leaf, last value is a predecessor')
            view.erase(hint_frame)
            return self.values.pop(-1), self
        else:
            view.draw_exp_text(self, f'Node [{self.id}] is not a leaf. Search for a predecessor in last child')
            view.hint_frame.move(self.children[-1].values[-1].x, self.children[-1].values[-1].y)
            view.erase(hint_frame)
            return self.children[-1].predecessor()

    def insert_and_fix(self, value, i):
        view = self.tree.view
        # Insert value
        if self.is_leaf:
            self.values.insert(i, value)
            value.x = self.x
            value.y = self.y - view.y_above
            self.values[i].parent = self
            view.draw_exp_text(self, f'Node [{self.id}] is a leaf. Insert {value.value} in the node [{self.id}]', False)
            self.tree.update_positions()
            view.animate(self)
        else:
            view.draw_exp_text(self, f'Insert value to a child node [{self.children[i].id}] of [{self.id}]', False)
            view.erase(hint_frame)
            view.move_object(grey_node, self.x, self.y, self.children[i].x, self.children[i].y)
            self.children[i].insert_value(value)
        # Fix AVB tree constraints
        if len(self.values) == self.tree.max_degree:
            view.erase(hint_frame)
            view.draw_exp_text(self, f'Number of values in [{self.id}] == max_tree_degree. Start fixing process')
            self.fix_insert()
