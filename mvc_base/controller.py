import copy
import tkinter as tk

import core.root as r
import mvc_base.history as h
from core.constants import canvas_width_modifier, canvas_height_modifier


def validate_input(val):
    if val.isdigit() and 0 <= int(val) <= 999:
        return True
    return False


class Controller:
    """Controller component of MVC design pattern"""

    def __init__(self, tree, view):
        self.tree = tree
        self.view = view
        self.history = h.History()

    def __deepcopy__(self, memo):
        return Controller(copy.deepcopy(self.tree), self.view)

    def clear(self):
        """
        Clears the tree and the view
        :return:
        """
        self.tree.clear()
        self.view.clear()
        self.history.clear()
        self.view.check_browsing_buttons(self.history.pointer, len(self.history.history_list))
        self.view.check_size_buttons()

    def perform(self, func, arg):
        """
        Performs a given action on the model(tree)
        :param func: action to perform
        :param arg: arguments for the action call
        :return: returns nothing
        """
        view = self.view
        view.set_buttons(False)
        view.set_browsing_buttons(False)
        add_final_result = False
        if validate_input(arg):
            val = int(arg)
            self.view.explanation_text.config(state=tk.NORMAL)
            self.view.explanation_text.delete(0.0, 'end')
            self.view.explanation_text.config(state=tk.DISABLED)
            if self.tree.root is not None and \
                    (func == r.Action.insert or
                     (func == r.Action.delete and self.tree.search_value_no_GUI(val) != (None, None))):
                add_final_result = True
                # Draw previous state on canvas_prev
                tree = self.history.get_elem()
                if tree is not None and tree.controller.tree.root is not None:
                    view.canvas_prev.delete('all')
                    tree = tree.controller.tree
                    tree.update_positions(True, width=int(r.frame.width * canvas_width_modifier))
                    view.draw_tree(tree.root, view.canvas_prev)
                    tree.root.update_positions(True)
                    self.history.pop()
                    self.history.append(h.HistoryElement(copy.deepcopy(self), func, arg))
            elif self.tree.root is None:
                add_final_result = True
                self.history.append(h.HistoryElement(copy.deepcopy(self), func, arg))
                view.canvas_prev.delete('all')
            if func == r.Action.insert:
                self.tree.insert_value(val)
            elif func == r.Action.delete:
                self.tree.delete_value(val)
            elif func == r.Action.search:
                self.tree.search_value(val)
            elif func == r.Action.min:
                self.tree.min()
            elif func == r.Action.max:
                self.tree.max()
            elif func == r.Action.mean:
                self.tree.mean()
            elif func == r.Action.median:
                self.tree.median()
            view.prepare_view()
            view.draw_tree(self.tree.root, view.canvas_now)
            if add_final_result:
                self.history.append(h.HistoryElement(copy.deepcopy(self), None, None))
        else:
            view.info_label.config(text='Not a valid input (integer in range 0-999)')
        view.set_buttons(True)
        view.set_browsing_buttons(True)
        self.view.check_browsing_buttons(self.history.pointer, len(self.history.history_list))
        view.check_size_buttons()

    def change_layout(self):
        """
        Switches between two and single canvas layout
        :return: returns nothing
        """
        view = self.view
        if view.layout == 'double':
            view.canvas_prev.pack_forget()
            view.prev_label.pack_forget()
            view.explanation_frame.grid_forget()
            view.width, view.height = int(1.25 * r.frame.width * canvas_width_modifier), 2 * int(
                r.frame.height * canvas_height_modifier)
            view.canvas_now.config(width=view.width, height=view.height)
            view.view_button.config(text='Show previous state and explanation: OFF')
            view.erase('all')
            if self.tree.root is not None:
                self.tree.root.update_positions(True, view.width)
            view.draw_tree(self.tree.root, view.canvas_now)
            view.layout = 'single'
        elif view.layout == 'single':
            view.canvas_now.pack_forget()
            view.now_label.pack_forget()
            view.prev_label.pack()
            view.canvas_prev.pack()
            view.now_label.pack()
            view.canvas_now.pack()
            view.explanation_frame.grid(row=0, column=0, sticky='NS')
            view.width = int(r.frame.width * canvas_width_modifier)
            view.height = int(r.frame.height * canvas_height_modifier)
            view.canvas_now.config(width=view.width, height=view.height)
            view.view_button.config(text='Show previous state and explanation: ON')
            view.erase('all')
            if self.tree.root is not None:
                self.tree.root.update_positions(True, view.width)
            view.draw_tree(self.tree.root, view.canvas_now)
            prev = self.history.get_prev()
            view.canvas_prev.delete('all')
            if prev is not None and prev.controller.tree.root is not None:
                prev.controller.tree.root.update_positions(True)
                prev = prev.controller.tree
                view.draw_tree(prev.root, view.canvas_prev, False)
            view.layout = 'double'

    def back(self):
        """Makes step back in browsing history"""
        self.view.erase('all')
        self.history.decrement()
        root = self.history.get_tree().root
        if root:
            root.update_positions(True)
        self.view.draw_tree(self.history.get_tree().root, self.view.canvas_now)
        self.view.check_browsing_buttons(self.history.pointer, len(self.history.history_list))

    def forward(self):
        """Makes step forward in browsing history --> performs an action from tree(time-1) state to tree(time) state"""
        history_elem = self.history.get_elem()
        cp = copy.deepcopy(history_elem.controller)
        cp.history.track = True
        # Draw tree(time-1) and perform action
        self.view.erase('all')
        self.view.canvas_prev.delete('all')
        self.view.draw_tree(cp.tree.root, self.view.canvas_now)
        self.view.draw_tree(cp.tree.root, self.view.canvas_prev)
        self.view.set_browsing_buttons(False)
        cp.perform(history_elem.func, history_elem.arg)
        self.view.set_browsing_buttons(True)
        cp.history.track = False
        # Draw tree(time)
        self.view.erase('all')
        self.history.increment()
        self.view.draw_tree(self.history.get_tree().root, self.view.canvas_now)
        self.view.check_browsing_buttons(self.history.pointer, len(self.history.history_list))
        # Draw most current tree if we are at the current history time moment
        if self.history.pointer == len(self.history.history_list) - 1:
            self.view.check_size_buttons()
            self.view.erase('all')
            self.view.draw_tree(self.tree.root, self.view.canvas_now)
