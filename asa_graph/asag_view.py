import tkinter as tk

import asa_graph.asag_model as asag
import mvc_base.view as view
from core.constants import green, white, black


class ASAGView(view.View):
    def __init__(self, node_width, node_height, columns_to_skip, current_max_degree):
        super().__init__(node_width, node_height, columns_to_skip)
        self.current_max_degree = current_max_degree

    def create_GUI(self, controller, text):
        """Adds max_degree selection"""
        frame = super().create_GUI(controller, text)

        def selector_change(*_):
            new_value = max_degree_value.get()
            if self.current_max_degree != new_value:
                self.current_max_degree = new_value
                controller.tree.clear()
                controller.tree = asag.ASAGraph(self, new_value)
                self.clear()

        max_degree_value = tk.IntVar(value=self.current_max_degree)
        max_degree_menu = tk.OptionMenu(self.controls_frame, max_degree_value, *[3, 4, 5, 6])
        max_degree_value.trace('w', selector_change)
        self.buttons.append(max_degree_menu)
        tk.Label(self.controls_frame, text='Max graph degree:').grid(row=0, column=0)
        max_degree_menu.grid(row=0, column=1, padx=(0, 20))
        return frame

    def draw_tree(self, node, canvas):
        if type(node) is asag.ASAGNode:
            canvas.create_text(node.values[0].x - 0.75 * self.node_width, node.y, fill=black, text=node.id,
                               tags=node.tag())
            for v in node.values:
                self.draw_object_with_children_lines(v, canvas)
            if not node.is_leaf:
                for c in node.children:
                    self.draw_tree(c, canvas)
        if node is not None and node is node.tree.root:
            in_order_list = node.in_order()
            for i in range(len(in_order_list) - 1):
                self.draw_line(canvas, in_order_list[i], in_order_list[i + 1], tk.SE, tk.SW, fill='blue')

    def draw_object_with_children_lines(self, obj, canvas):
        parent = obj.parent
        if not parent.is_leaf:
            index = parent.values.index(obj)
            self.draw_line(canvas, obj, parent.children[index], tk.SW, tk.N)
            if index == len(parent.values) - 1:
                self.draw_line(canvas, obj, parent.children[index + 1], tk.SE, tk.N)
        self.draw_object(obj, canvas)

    def draw_object(self, node, canvas):
        if type(node) is not None:
            canvas.create_rectangle(node.x - self.node_width // 2, node.y - self.node_height // 2,
                                    node.x + self.node_width // 2, node.y + self.node_height // 2,
                                    fill=green, tags=node.tag())
            canvas.create_text(node.x, node.y, fill=white, text=node.value, tags=node.tag())
            canvas.create_text(node.x, node.y + self.node_height, fill=black, text=f'[{node.counter}]',
                               font=(None, 8), tags=node.tag())
