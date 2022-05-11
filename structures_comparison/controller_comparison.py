import copy
import threading

import core.root as r
import mvc_base.history as h
from mvc_base.controller import validate_input


class ComparisonController:
    """Controller component of MVC design pattern"""

    def __init__(self, view):
        self.view = view
        self.history = h.History()
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
        self.history.clear()
        self.view.clear()

    def perform(self, func, arg):
        """
        Performs a given action on the models(trees)
        :param func: action to perform
        :param arg: arguments for the action call
        :return: returns nothing
        """
        view = self.view
        add_final_result = False
        view.animation_controller.reset()
        if validate_input(arg):
            val = int(arg)
            self.top_finished, self.bottom_finished = False, False
            view.set_buttons(False)
            # History management
            if self.top_tree.root is not None and \
                    (func == r.Action.insert or
                     (func == r.Action.delete and self.top_tree.search_value_no_GUI(val) != (None, None))):
                add_final_result = True
                # Draw previous state on canvas_prev
                tree = self.history.get_elem()
                if tree is not None and tree.controller.top_tree.root is not None:
                    self.history.pop()
                    self.history.append(h.HistoryElement(copy.deepcopy(self), func, arg))
            elif self.top_tree.root is None:
                add_final_result = True
                self.history.append(h.HistoryElement(copy.deepcopy(self), func, arg))

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
            self.bottom_finished = True
            self.view.canvas_bottom.delete('all')
            self.bottom_tree.view.draw_tree(self.bottom_tree.root, view.canvas_bottom)
            if add_final_result:
                self.history.append(h.HistoryElement(copy.deepcopy(self), None, None))
        else:
            view.info_label.config(text='Not a valid input (integer in range 0-999)')
        self.check_buttons()

    def back(self):
        """Makes step back in browsing history"""
        self.view.erase()
        self.history.decrement()
        top_root = self.history.get_elem().controller.top_tree.root
        bottom_root = self.history.get_elem().controller.bottom_tree.root
        if top_root:
            top_root.update_positions(True)
        if bottom_root:
            bottom_root.update_positions(True)
        self.history.get_elem().controller.top_tree.view.draw_tree(self.history.get_elem().controller.top_tree.root,
                                                                   self.view.canvas_top)
        self.history.get_elem().controller.bottom_tree.view.draw_tree(
            self.history.get_elem().controller.bottom_tree.root, self.view.canvas_bottom)
        self.view.set_buttons(False)
        self.view.check_browsing_buttons(self.history.pointer, len(self.history.history_list))

    def forward(self):
        """Makes step forward in browsing history --> performs an action from tree(time-1) state to tree(time) state"""
        history_elem = self.history.get_elem()
        cp = copy.deepcopy(history_elem.controller)
        cp.history.track = True
        # Draw tree(time-1) and perform action
        self.view.erase()
        self.history.get_elem().controller.top_tree.view.draw_tree(cp.top_tree.root, self.view.canvas_top)
        self.history.get_elem().controller.bottom_tree.view.draw_tree(cp.bottom_tree.root, self.view.canvas_bottom)
        self.view.set_browsing_buttons(False)
        cp.perform(history_elem.func, history_elem.arg)
        self.view.set_browsing_buttons(True)
        cp.history.track = False
        # Draw tree(time)
        self.view.canvas_top.delete('all')
        self.history.increment()
        self.history.get_elem().controller.top_tree.view.draw_tree(self.history.get_elem().controller.top_tree.root,
                                                                   self.view.canvas_top)
        self.history.get_elem().controller.bottom_tree.view.draw_tree(
            self.history.get_elem().controller.bottom_tree.root, self.view.canvas_bottom)
        self.view.set_buttons(False)
        self.view.check_browsing_buttons(self.history.pointer, len(self.history.history_list))
        # Draw most current tree if we are at the current history time moment
        if self.history.pointer == len(self.history.history_list) - 1:
            self.check_buttons()
            self.view.check_size_buttons()
            self.view.canvas_top.delete('all')
            self.history.get_elem().controller.top_tree.view.draw_tree(self.top_tree.root, self.view.canvas_top)
            self.history.get_elem().controller.bottom_tree.view.draw_tree(self.bottom_tree.root,
                                                                          self.view.canvas_bottom)

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
            self.view.check_browsing_buttons(self.history.pointer, len(self.history.history_list))
            self.view.check_size_buttons()
        else:
            r.frame.after(10, self.check_buttons)
