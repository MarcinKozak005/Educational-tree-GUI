import abc
import tkinter as tk

import core.root as r
import mvc_base.model_multi_child as mc
from core.constants import blue


class BalValue(mc.MCValue):

    def __init__(self, value, parent_node, x=0, y=0):
        super().__init__(value, parent_node, x, y)


class LinkBalValue(BalValue):
    def __init__(self, value, parent_node, x=0, y=0):
        super().__init__(value, parent_node, x, y)
        self.prev_value = None
        self.next_value = None

    def rewrite(self):
        if self.prev_value is not None:
            self.prev_value.next_value = self.next_value
        if self.next_value is not None:
            self.next_value.prev_value = self.prev_value

    def tick(self, view, x_unit, y_unit):
        super().tick(view, x_unit, y_unit)
        if self.next_value is not None:
            view.draw_line(view.canvas_now, self, self.next_value, tk.SE, tk.SW, fill=blue)


class BalTree(mc.MCTree, abc.ABC):
    pass


class BalNode(mc.MCNode, abc.ABC):

    def insert_value(self, value):
        """
        Inserts value in the node or calls insert on child node to which the value should be inserted
        :param value: value to insert
        :return: returns nothing
        """
        i = 0
        view = self.tree.view
        view.hint_frame.draw(self.values[0].x, self.values[0].y)
        # Search for a spot to insert new value
        while i < len(self.values) and value.value >= self.values[i].value:
            view.draw_exp_text(self.values[i],
                               f'[{self.id}]: {value.value} >= {self.values[i].value}, check next value',
                               False)
            view.hint_frame.move(self.values[i].x + view.node_width, self.values[i].y, True)
            i += 1
        # Show end-search reason
        if i < len(self.values):
            view.draw_exp_text(self.values[i], f'[{self.id}]: {value.value} < {self.values[i].value}, '
                                               f'insert before {self.values[i].value}', False)
            view.hint_frame.move(self.values[i].x - view.node_width // 2, self.values[i].y, True)
        else:
            view.draw_exp_text(self, f'No next value', False)
            view.hint_frame.move(self.values[-1].x + view.node_width // 2, self.values[-1].y, True)
        self.insert_and_fix(value, i)

    @abc.abstractmethod
    def split_child(self, i, full_node):
        pass

    def get_next(self, position, mode=r.Mode.down):
        """
        Get the next_value - such that after sorting values next_value would be just after self
        :param position: position of node/value we want to get next of
        :param mode: Mode.down or Mode.up
        :return: returns next_value or None if it's not found
        """

        def get_next_help(node):
            if node.parent is not None:
                return node.parent.get_next(node.parent.children.index(node), r.Mode.up)
            else:
                return None

        if position is None:
            return None

        if mode == r.Mode.down:
            if self.is_leaf:
                if position + 1 < len(self.values):
                    return self.values[position + 1]
                # search in nodes above
                else:
                    return get_next_help(self)
            else:
                return self.children[position + 1].get_next(-1, r.Mode.down)
        elif mode == r.Mode.up:
            if position + 1 < len(self.children):
                return self.children[position + 1].get_next(-1, r.Mode.down)
            # search in nodes above
            else:
                return get_next_help(self)

    def get_prev(self, position, mode=r.Mode.down):
        """
        Get the prev_value - such that after sorting values prev_value would be just before self
        :param position: position of node/value we want to get next of
        :param mode: Mode.down or Mode.up
        :return: returns prev_value or None if it's not found
        """

        def get_prev_help(node):
            if node.parent is not None:
                return node.parent.get_prev(node.parent.children.index(node), r.Mode.up)
            else:
                return None

        if position is None:
            return None

        if mode == r.Mode.down:
            if self.is_leaf:
                if position - 1 >= 0:
                    return self.values[position - 1]
                # search in nodes above
                else:
                    return get_prev_help(self)
            else:
                return self.children[position].get_prev(len(self.children[position].values), r.Mode.down)
        elif mode == r.Mode.up:
            if position != 0:
                return self.children[position - 1].get_prev(len(self.children[position - 1].values), r.Mode.down)
            # search in nodes above
            else:
                return get_prev_help(self)
