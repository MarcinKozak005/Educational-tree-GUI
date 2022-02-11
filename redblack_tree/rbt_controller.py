import copy
import redblack_tree.rbt_model as rbt

def validate_input(val):
    if val.isdigit() and 0 <= int(val) <= 999:
        return True
    return False


class Controller:
    def __init__(self, tree, view):
        self.tree = tree
        self.tree_copy = rbt.RBTree(None)
        self.view = view

    def copy_tree(self):
        self.tree_copy.root = copy.deepcopy(self.tree.root)
        self.tree_copy.view = self.tree.view

    def clear(self):
        self.tree.clear()
        self.view.clear()

    def perform(self, obj, func, arg):
        self.view.set_buttons(False)  # To do controllera
        if validate_input(arg):
            if self.tree.root is not None:
                self.view.canvas_prev.delete('all')
                self.tree.root.update_positions(self.tree.root, True, width=800)
                self.view.draw_rb_tree(self.tree.root, self.view.canvas_prev)
                self.tree.root.update_positions(self.tree.root, True)
            func(obj, int(arg))
        else:
            self.view.info_label.config(text='Not a valid input (integer in range 0-999)')
        self.view.set_buttons(True)

    def change_layout(self):
        view = self.view
        if view.layout == 'double':
            view.canvas_prev.pack_forget()
            view.prev_label.pack_forget()
            view.frame31.grid_forget()
            view.width, view.height = 1400, 600
            view.canvas_now.config(width=view.width, height=view.height)
            view.view_button.config(text='Show previous state and explanation: OFF')
            view.canvas_now.delete('all')
            self.tree.root.update_positions(self.tree.root, True)
            view.draw_rb_tree(self.tree.root, view.canvas_now)
            view.layout = 'single'
        elif view.layout == 'single':
            view.canvas_now.pack_forget()
            view.now_label.pack_forget()
            view.prev_label.pack()
            view.canvas_prev.pack()
            view.now_label.pack()
            view.canvas_now.pack()
            view.frame31.grid(row=0, column=0, sticky='NS')
            view.width, view.height = 800, 300
            view.canvas_now.config(width=view.width, height=view.height)
            view.view_button.config(text='Show previous state and explanation: ON')
            view.canvas_now.delete('all')
            # view.canvas_prev.delete('all')
            self.tree.root.update_positions(self.tree.root, True)
            # update_positions(rb_tree_root_copy, True)
            view.draw_rb_tree(self.tree.root, view.canvas_now)
            # draw_rb_tree(rb_tree_root_copy, canvas_prev)
            view.layout = 'double'
