# Contains base classes for model components of MVC design pattern
import abc


class Tree(abc.ABC):
    """Base class for all trees"""

    def __init__(self, view):
        self.root = None
        self.view = view

    @property
    @abc.abstractmethod
    def node_class(self):
        pass

    @abc.abstractmethod
    def insert_value(self, value):
        """
        Inserts value into the tree
        :param value: value to be inserted
        :return: returns nothing
        """
        pass

    @abc.abstractmethod
    def delete_value(self, value):
        """
        Deletes value from the tree
        :param value: value to be deleted
        :return: returns nothing
        """
        pass

    @abc.abstractmethod
    def search_value(self, value):
        """
        Searches for the value in the tree. Shows the process in the GUI
        :param value: value to be searched for
        :return: returns nothing
        """
        pass

    @abc.abstractmethod
    def search_value_no_GUI(self, value):
        """
        Searches for the value in the tree. Does not show the process in the GUI
        :param value: value to be found
        :return: found node or node and position of found value or tuple: None, None
        """
        pass

    @abc.abstractmethod
    def clear(self):
        """
        Resets tree attributes
        :return: returns nothing
        """
        pass

    @abc.abstractmethod
    def min(self):
        """:return: Returns minimal element in the tree"""
        pass

    @abc.abstractmethod
    def max(self):
        """:return: Returns maximal element in the tree"""
        pass

    @abc.abstractmethod
    def mean(self):
        """:return: Returns mean value of the tree elements"""
        pass

    @abc.abstractmethod
    def median(self):
        """:return: Returns median value of the tree elements"""
        pass

    def update_positions(self, static=False, width=None):
        if self.root is not None:
            self.root.update_positions(static, width)



class AnimatedObject(abc.ABC):
    """Base class for all animated objects"""
    def __init__(self, x, y, parent):
        self.parent = parent
        self.x = x
        self.y = y
        self.x_next = x
        self.y_next = y

    @abc.abstractmethod
    def tick(self, view, x_unit, y_unit):
        """
        Performs the smallest animation move
        :return: returns nothing
        """
        pass

    @abc.abstractmethod
    def tag(self):
        """
        :return: returns object tag, by which it cen be referenced on canvas
        """
        pass


class Node(abc.ABC):
    """Base class for node like structures"""
    def __init__(self, tree, l_edge, r_edge):
        self.tree = tree
        # For visualization: space between l_edge and r_edge is where all node's children will be placed
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
        """
        Updates the node's positions and if applicable it's children nodes / value
        :param static: True means there will be no animation, False means there will be an animation
        :param width: width of canvas for updating positions
        :return: returns nothing
        """
        pass

    @abc.abstractmethod
    def successors(self):
        """
        Get the list of all successors of the node (nodes and if applicable values)
        :return: list of successors
        """
        pass

    @abc.abstractmethod
    def successor(self):
        pass


    @abc.abstractmethod
    def min(self):
        """:return: Returns minimal element in the tree"""
        pass

    @abc.abstractmethod
    def max(self):
        """:return: Returns maximal element in the tree"""
        pass

    @abc.abstractmethod
    def mean(self, val_sum, counter):
        """:return: Returns mean value of the tree elements"""
        pass

    @abc.abstractmethod
    def median(self, tab):
        """:return: Returns median value of the tree elements"""
        pass
