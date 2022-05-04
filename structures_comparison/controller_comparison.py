import copy
import threading

import core.root as r
from mvc_base.controller import validate_input, History


class ComparisonController:
    """Controller component of MVC design pattern"""

    def __init__(self, view):
        self.top_tree = None
        self.top_tree_degree = 3
        self.top_structure = None
        self.bottom_tree = None
        self.bottom_structure = None
        self.bottom_tree_degree = 3
        self.view = view
        self.history = History()

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
        if validate_input(arg):
            val = int(arg)
            if func == r.Action.insert:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.insert_value(val))).start()
                self.bottom_tree.insert_value(val)
            elif func == r.Action.delete:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.delete_value(val))).start()
                self.bottom_tree.delete_value(val)
            elif func == r.Action.search:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.search_value(val))).start()
                self.bottom_tree.search_value(val)
            elif func == r.Action.min:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.min())).start()
                self.bottom_tree.min()
            elif func == r.Action.max:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.max())).start()
                self.bottom_tree.max()
            elif func == r.Action.mean:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.mean())).start()
                self.bottom_tree.mean()
            elif func == r.Action.median:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.median())).start()
                self.bottom_tree.median()
            self.view.canvas_bottom.delete('all')
            self.bottom_tree.view.draw_tree(self.bottom_tree.root, view.canvas_bottom)
        else:
            view.info_label.config(text='Not a valid input (integer in range 0-999)')

    def back(self):
        pass

    def forward(self):
        pass

    def top_canvas_draw(self, func):
        func()
        self.view.canvas_top.delete('all')
        self.top_tree.view.draw_tree(self.top_tree.root, self.view.canvas_top)
