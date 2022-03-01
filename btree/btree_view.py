import tkinter as tk
import btree.btree_model as btree
import mvc_base.view as view


class BTView(view.View):
    def __init__(self, node_width, node_height, columns_to_skip, current_max_degree):
        super().__init__(node_width, node_height, columns_to_skip)
        self.current_max_degree = current_max_degree

    def create_GUI(self, controller):
        frame = super().create_GUI(controller)

        def selector_change(*_):
            new_value = max_degree_value.get()
            if self.current_max_degree != new_value:
                self.current_max_degree = new_value
                controller.tree = btree.BTree(new_value, self)
                self.clear()

        max_degree_value = tk.IntVar(value=self.current_max_degree)
        max_degree_menu = tk.OptionMenu(self.controls_frame, max_degree_value, *[3, 4, 5, 6])
        max_degree_value.trace('w', selector_change)
        tk.Label(self.controls_frame, text='Max tree degree:').grid(row=0, column=0)
        max_degree_menu.grid(row=0, column=1, padx=(0, 20))

        return frame

    def draw_tree(self, node, canvas):
        """
        Draws node and it's left/right subtrees
        :param node: node to draw
        :param canvas: canvas on which node will be drawn
        :return: returns nothing
        """
        if type(node) is btree.BTNode:
            canvas.create_text(node.values[0].x - 0.75 * self.node_width, node.y, fill='black', text=node.id,
                               tags=f'Node{hash(node)}')
            for v in node.values:
                self.draw_object_with_children_lines(v, canvas)
            if not node.is_leaf:
                for c in node.children:
                    self.draw_tree(c, canvas)

    def draw_object_with_children_lines(self, obj, canvas):
        """
        Draws node with children lines
        :param obj: object
        :param canvas: canvas on which node will be drawn
        :return: returns nothing
        """
        value = obj
        node = value.parent
        if not node.is_leaf:
            index = node.values.index(value)
            self.draw_line(canvas, value, node.children[index], tk.SW, tk.N)
            if index == len(node.values) - 1:
                self.draw_line(canvas, value, node.children[index + 1], tk.SE, tk.N)
        self.draw_object(value, canvas)

    def draw_object(self, node, canvas):
        """
        Draws the node
        :param node: node to be drawn
        :param canvas: canvas on which the node will be drawn
        :return: returns nothing
        """
        if type(node) is btree.BTValue:
            canvas.create_rectangle(node.x - self.node_width // 2, node.y - self.node_height // 2,
                                    node.x + self.node_width // 2, node.y + self.node_height // 2, fill='green',
                                    tags=f'Value{hash(node)}')
            canvas.create_text(node.x, node.y, fill='white', text=node.value, tags=f'Value{hash(node)}')


