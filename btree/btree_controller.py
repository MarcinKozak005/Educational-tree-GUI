import core.root as r


def validate_input(val):
    if val.isdigit() and 0 <= int(val) <= 999:
        return True
    return False


class Controller:
    def __init__(self, tree, view):
        self.tree = tree
        self.view = view

    def clear(self):
        """
        Clears the tree and the view
        :return:
        """
        self.tree.clear()
        self.view.clear()

    def perform(self, func, arg):
        """
        Performs a given action on the model(tree)
        :param func: action to perform
        :param arg: arguments for the action call
        :return: returns nothing
        """
        self.view.set_buttons(False)
        if validate_input(arg):
            val = int(arg)
            if self.tree.root is not None and (func == r.Action.insert or func == r.Action.delete and self.tree.search_value_no_GUI(val)):
                self.view.canvas_prev.delete('all')
                self.tree.root.update_positions(True, width=1000)
                self.view.draw_btree(self.tree.root, self.view.canvas_prev)
                self.tree.root.update_positions(True)
            if func == r.Action.insert:
                self.tree.insert_value(val)
            elif func == r.Action.delete:
                self.tree.delete_value(val)
            elif func == r.Action.search:
                self.tree.search_value(val)
            self.view.prepare_view()
            self.view.draw_btree(self.tree.root, self.view.canvas_now)
        else:
            self.view.info_label.config(text='Not a valid input (integer in range 0-999)')
        self.view.set_buttons(True)

    def change_layout(self):
        view = self.view
        if view.layout == 'double':
            view.canvas_prev.pack_forget()
            view.prev_label.pack_forget()
            view.explanation_frame.grid_forget()
            view.width, view.height = 1400, 600
            view.canvas_now.config(width=view.width, height=view.height)
            view.view_button.config(text='Show previous state and explanation: OFF')
            view.canvas_now.delete('all')
            if self.tree.root is not None:
                self.tree.root.update_positions(True, view.width)
            view.draw_rb_tree(self.tree.root, view.canvas_now)
            view.layout = 'single'
        elif view.layout == 'single':
            view.canvas_now.pack_forget()
            view.now_label.pack_forget()
            view.prev_label.pack()
            view.canvas_prev.pack()
            view.now_label.pack()
            view.canvas_now.pack()
            view.explanation_frame.grid(row=0, column=0, sticky='NS')
            view.width, view.height = 1000, 300
            view.canvas_now.config(width=view.width, height=view.height)
            view.view_button.config(text='Show previous state and explanation: ON')
            view.canvas_now.delete('all')
            if self.tree.root is not None:
                self.tree.root.update_positions(True, view.width)
            view.draw_rb_tree(self.tree.root, view.canvas_now)
            view.layout = 'double'