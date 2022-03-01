import abc


class Tree(abc.ABC):

    def __init__(self, view):
        self.root = None
        self.view = view

    @abc.abstractmethod
    def insert_value(self, value):
        pass

    @abc.abstractmethod
    def delete_value(self, value):
        pass

    @abc.abstractmethod
    def search_value(self, value):
        pass

    @abc.abstractmethod
    def search_value_no_GUI(self, value):
        pass

    @abc.abstractmethod
    def update_positions(self, static=False, width=None):
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def print_tree(self):
        pass


class AnimatedObject(abc.ABC):
    def __init__(self, x, y, parent):
        self.parent = parent
        self.x = x
        self.y = y
        self.x_next = x
        self.y_next = y

    @abc.abstractmethod
    def tick(self, view, x_unit, y_unit):
        """
        Performs the smallest move from the rotation
        :return: returns nothing
        """
        pass


class Node:
    def __init__(self, tree, l_edge, r_edge):
        self.tree = tree
        self.l_edge = l_edge
        self.r_edge = r_edge

    @abc.abstractmethod
    def insert_value(self, value):
        pass

    @abc.abstractmethod
    def delete_value(self, value):
        pass

    @abc.abstractmethod
    def search_value(self, value):
        pass

    @abc.abstractmethod
    def search_value_no_GUI(self, value):
        pass

    @abc.abstractmethod
    def update_positions(self, static=False, width=None):
        pass

    @abc.abstractmethod
    def successors(self):
        pass

    @abc.abstractmethod
    def successor(self):
        pass

    @abc.abstractmethod
    def print_node(self, indent):
        pass
