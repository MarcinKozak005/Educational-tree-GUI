import copy
import threading

import core.root as r
from mvc_base.controller import validate_input, History


class ComparisonController:
    """Controller component of MVC design pattern"""

    def __init__(self, view):
        self.view = view
        self.history = History()
        # Top
        self.top_tree = None
        self.top_tree_degree = 3
        self.top_structure = r.Structure.RBT
        self.top_finished = True
        # Bottom
        self.bottom_tree = None
        self.bottom_structure = r.Structure.AVL
        self.bottom_tree_degree = 3
        self.bottom_finished = True

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
            self.top_finished, self.bottom_finished = False, False
            view.set_buttons(False)
            if func == r.Action.insert:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.insert_value(val))).start()
                r.wait(200)
                self.bottom_tree.insert_value(val)
            elif func == r.Action.delete:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.delete_value(val))).start()
                r.wait(200)
                self.bottom_tree.delete_value(val)
            elif func == r.Action.search:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.search_value(val))).start()
                r.wait(200)
                self.bottom_tree.search_value(val)
            elif func == r.Action.min:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.min())).start()
                r.wait(200)
                self.bottom_tree.min()
            elif func == r.Action.max:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.max())).start()
                r.wait(200)
                self.bottom_tree.max()
            elif func == r.Action.mean:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.mean())).start()
                r.wait(200)
                self.bottom_tree.mean()
            elif func == r.Action.median:
                threading.Thread(target=lambda: self.top_canvas_draw(lambda: self.top_tree.median())).start()
                r.wait(200)
                self.bottom_tree.median()
            self.bottom_finished = True
            self.view.canvas_bottom.delete('all')
            self.bottom_tree.view.draw_tree(self.bottom_tree.root, view.canvas_bottom)
        else:
            view.info_label.config(text='Not a valid input (integer in range 0-999)')
        self.check_buttons()

    def back(self):
        pass

    def forward(self):
        pass

    def top_canvas_draw(self, func):
        func()
        self.view.canvas_top.delete('all')
        self.top_tree.view.draw_tree(self.top_tree.root, self.view.canvas_top)
        self.top_finished = True

    def check_buttons(self):
        if self.top_finished and self.bottom_finished:
            self.view.set_buttons(True)
            if self.top_structure in (r.Structure.RBT, r.Structure.AVL):
                self.view.set_buttons_degree(r.Mode.up, False)
            else:
                self.view.set_buttons_degree(r.Mode.up, True, self.top_tree_degree)

            if self.bottom_structure in (r.Structure.RBT, r.Structure.AVL):
                self.view.set_buttons_degree(r.Mode.down, False)
            else:
                self.view.set_buttons_degree(r.Mode.down, True, self.bottom_tree_degree)
        else:
            r.frame.after(10, self.check_buttons)
