import copy

import core.root as r
from mvc_base.controller import validate_input


class ComparisonController:
    """Controller component of MVC design pattern"""

    def __init__(self, view):
        self.top_tree = None
        self.bottom_tree = None
        self.view = view

    def __deepcopy__(self, memo):
        c = ComparisonController(self.view)
        c.top_tree = copy.deepcopy(self.top_tree)
        c.bottom_tree = copy.deepcopy(self.bottom_tree)
        return c

    def clear(self):
        """
        Clears the trees and the view
        :return:
        """
        self.top_tree.clear()
        self.bottom_tree.clear()
        self.view.clear()

    def perform(self, func, arg):
        """
        Performs a given action on the models(trees)
        :param func: action to perform
        :param arg: arguments for the action call
        :return: returns nothing
        """
        view = self.view
        view.set_buttons(False)
        if validate_input(arg):
            val = int(arg)
            if func == r.Action.insert:
                self.top_tree.insert_value(val)
                self.bottom_tree.insert_value(val)
            elif func == r.Action.delete:
                self.top_tree.delete_value(val)
                self.bottom_tree.delete_value(val)
            elif func == r.Action.search:
                self.top_tree.search_value(val)
                self.bottom_tree.search_value(val)
            elif func == r.Action.min:
                self.top_tree.min()
                self.bottom_tree.min()
            elif func == r.Action.max:
                self.top_tree.max()
                self.bottom_tree.max()
            elif func == r.Action.mean:
                self.top_tree.mean()
                self.bottom_tree.mean()
            elif func == r.Action.median:
                self.top_tree.median()
                self.bottom_tree.median()
            view.prepare_view()
            view.draw_tree(self.top_tree.root, view.canvas_top)
            view.draw_tree(self.bottom_tree.root, view.canvas_bottom)
        else:
            view.info_label.config(text='Not a valid input (integer in range 0-999)')
        view.set_buttons(True)

    def back(self):
        pass

    def forward(self):
        pass
