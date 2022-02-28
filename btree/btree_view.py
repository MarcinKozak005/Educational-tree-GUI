import tkinter as tk
import core.root as r
import btree.btree_model as bt
import redblack_tree.rbt_model as rbt
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
                controller.tree = bt.BTree(new_value, self)
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
        if type(node) is bt.BTree.BTreeNode:
            canvas.create_text(node.values[0].x - 0.75 * self.node_width, node.y, fill='black', text=node.id,
                               tags=f'Node{hash(node)}')
            for v in node.values:
                self.draw_node_with_children_lines(v, node, canvas)
            if not node.is_leaf:
                for c in node.children:
                    self.draw_btree(c, canvas)

    def draw_node_with_children_lines(self, value, node, canvas):
        """
        Draws node with children lines
        :param value: value object
        :param node: node to draw
        :param canvas: canvas on which node will be drawn
        :return: returns nothing
        """
        if type(value) is bt.BTree.BTreeNode.BValue:
            if not node.is_leaf:
                index = node.values.index(value)
                self.draw_line(canvas, value, node.children[index], tk.SW, tk.N)
                if index == len(node.values) - 1:
                    self.draw_line(canvas, value, node.children[index + 1], tk.SE, tk.N)
            self.draw_node(value, canvas)

    def side_modifier(self, side):
        if side == tk.NE:
            sides = [tk.N, tk.E]
        elif side == tk.SE:
            sides = [tk.S, tk.E]
        elif side == tk.SW:
            sides = [tk.S, tk.W]
        elif side == tk.NW:
            sides = [tk.N, tk.W]
        else:
            sides = [side]

        x_mod = 0
        y_mod = 0
        if tk.N in sides:
            y_mod -= self.node_height // 2
        if tk.E in sides:
            x_mod += self.node_width // 2
        if tk.S in sides:
            y_mod += self.node_height // 2
        if tk.W in sides:
            x_mod -= self.node_width // 2
        return x_mod, y_mod

    def draw_line(self, canvas, node1, node2, from_side=tk.CENTER, to_side=tk.CENTER):
        """
        Draws a line between two nodes
        :param canvas: canvas to draw on
        :param node1: from-node
        :param node2: to-node
        :return: returns nothing
        """
        if node1 is not None and node2 is not None and type(node1) is not rbt.RBTree.RBLeaf \
                and type(node2) is not rbt.RBTree.RBLeaf:
            from_mod = self.side_modifier(from_side)
            to_mod = self.side_modifier(to_side)
            canvas.create_line(node1.x + from_mod[0], node1.y + from_mod[1], node2.x + to_mod[0], node2.y + to_mod[1],
                               fill='black', tags=[f'Line{hash(node1)}', 'Line'])

    def draw_node(self, node, canvas):
        """
        Draws the node
        :param node: node to be drawn
        :param canvas: canvas on which the node will be drawn
        :return: returns nothing
        """
        if type(node) is bt.BTree.BTreeNode.BValue:
            canvas.create_rectangle(node.x - self.node_width // 2, node.y - self.node_height // 2,
                                    node.x + self.node_width // 2, node.y + self.node_height // 2, fill='green',
                                    tags=f'Value{hash(node)}')
            canvas.create_text(node.x, node.y, fill='white', text=node.value, tags=f'Value{hash(node)}')

    def animate_values_movement(self, node):
        def values_tick(v, x_un, y_un):
            self.canvas_now.delete(f'Line{hash(v)}')
            if self.canvas_now.find_withtag(f'Value{hash(v)}'):
                self.canvas_now.move(f'Value{hash(v)}', x_un, y_un)
            else:
                self.canvas_now.move(f'grey_node', x_un, y_un)
            v.x += x_un
            v.y += y_un
            index = v.parent.values.index(v)
            if not v.parent.is_leaf:
                if index < len(node.children):
                    self.draw_line(self.canvas_now, v, v.parent.children[index], tk.SW, tk.N)
                if index == len(node.values) - 1 and index + 1 < len(node.children):
                    self.draw_line(self.canvas_now, v, v.parent.children[index + 1], tk.SE, tk.N)
                self.canvas_now.tag_lower('Line')

        def nodes_tick(n, x_un, y_un):
            self.canvas_now.move(f'Node{hash(n)}', x_un, y_un)
            n.x += x_un
            n.y += y_un

        if node is not None:
            successors = node.successors()
            units = {}
            tmp = self.animation_time / self.animation_unit
            for s in successors:
                x_unit = (s.x_next - s.x) / tmp
                y_unit = (s.y_next - s.y) / tmp
                units[s] = (x_unit, y_unit)
            while tmp > 0:
                for s in successors:
                    if type(s) is bt.BTree.BTreeNode.BValue:
                        values_tick(s, units[s][0], units[s][1])
                    elif type(s) is bt.BTree.BTreeNode:
                        nodes_tick(s, units[s][0], units[s][1])
                r.wait(self.animation_unit)
                tmp -= 1
