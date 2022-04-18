import tkinter as tk

import bt.bt_model as bt
import mvc_base.model_balanced as mb
import mvc_base.view as view
from core.constants import white, black


class BTView(view.View):
    def __init__(self, node_width, node_height, columns_to_skip, current_max_degree):
        super().__init__(node_width, node_height, columns_to_skip)
        self.current_max_degree = current_max_degree

    def create_GUI(self, controller, text):
        """Adds max_degree selection"""
        frame = super().create_GUI(controller, text)
        self.add_max_degree_change_to_GUI(controller)
        return frame

    def draw_tree(self, node, canvas):
        if type(node) is bt.BTNode:
            canvas.create_text(node.values[0].x - 0.75 * self.node_width, node.y, fill=black, text=node.id,
                               tags=node.tag(), font=('TkDefaultFont', 10, 'bold'))
            for v in node.values:
                self.draw_object_with_children_lines(v, canvas)
            if not node.is_leaf:
                for c in node.children:
                    self.draw_tree(c, canvas)

    def draw_object_with_children_lines(self, obj, canvas):
        parent = obj.parent
        if not parent.is_leaf:
            index = parent.values.index(obj)
            self.draw_line(canvas, obj, parent.children[index], tk.SW, tk.N)
            if index == len(parent.values) - 1:
                self.draw_line(canvas, obj, parent.children[index + 1], tk.SE, tk.N)
        self.draw_object(obj, canvas)

    def draw_object(self, node, canvas):
        if type(node) is mb.BalValue:
            canvas.create_image(node.x - self.node_width // 2, node.y - self.node_height // 2,
                                image=node.parent.tree.green_square, anchor='nw', tags=node.tag())
            canvas.create_text(node.x, node.y, fill=white, text=node.value, tags=node.tag(),
                               font=('TkDefaultFont', 10, 'bold'))
