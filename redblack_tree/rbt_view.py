import core.root as r
import redblack_tree.rbt_model as rbt
import mvc_base.view as view


class RBTView(view.View):
    def __init__(self, node_width, node_height, columns_to_skip):
        super().__init__(node_width, node_height, columns_to_skip)

    def draw_recolor_text(self, node, to_color):
        """
        Draws the recoloring info on the node
        :param node: the node to be recolored
        :param to_color: color to which the node is recolored
        :return: returns nothing
        """
        if type(node) is rbt.RBTNode:
            txt = self.canvas_now.create_text(node.x, node.y - self.node_height,
                                              fill='white',
                                              text=f'Change color to {to_color}',
                                              tags='recolor_txt')
            txt_bg = self.canvas_now.create_rectangle(self.canvas_now.bbox(txt), fill="grey", tags='recolor_txt')
            self.explanation.append(f'Change color of {node.value} to {to_color}')
            self.canvas_now.tag_lower(txt_bg)

    def draw_tree(self, node, canvas):
        """
        Draws node and it's left/right subtrees
        :param node: node to draw
        :param canvas: canvas on which node will be drawn
        :return: returns nothing
        """
        if type(node) is not rbt.RBTLeaf and node is not None:
            self.draw_node_with_children_lines(node, canvas)
            self.draw_rb_tree(node.left, canvas)
            self.draw_rb_tree(node.right, canvas)

    def draw_node_with_children_lines(self, node, canvas):
        """
        Draws node with children lines
        :param node: node to draw
        :param canvas: canvas on which node will be drawn
        :return: returns nothing
        """
        if type(node) is not rbt.RBTLeaf:
            if type(node.right) is not rbt.RBTLeaf:
                self.draw_line(canvas, node, node.right)
            if type(node.left) is not rbt.RBTLeaf:
                self.draw_line(canvas, node, node.left)
            self.draw_node(node, canvas)

    def draw_line(self, canvas, node1, node2):
        """
        Draws a line between two nodes
        :param canvas: canvas to draw on
        :param node1: from-node
        :param node2: to-node
        :return: returns nothing
        """
        if node1 is not None and node2 is not None and type(node1) is not rbt.RBTLeaf \
                and type(node2) is not rbt.RBTLeaf:
            canvas.create_line(node1.x, node1.y, node2.x, node2.y, fill='black',
                               tags=[f'Line{hash(node1)}', 'Line'])

    def draw_node(self, node, canvas):
        """
        Draws the node
        :param node: node to be drawn
        :param canvas: canvas on which the node will be drawn
        :return: returns nothing
        """
        if type(node) is rbt.RBTNode:
            canvas.create_oval(node.x - self.node_width // 2, node.y - self.node_height // 2,
                               node.x + self.node_width // 2,
                               node.y + self.node_height // 2, fill=node.color, tags=f'Node{hash(node)}')
            canvas.create_text(node.x, node.y, fill='white', text=node.value, tags=f'Node{hash(node)}')

    def animate_rotations(self, node):
        """
        Animates red-black tree rotations
        :param node: node to start the rotation process
        :return: returns nothing
        """

        def rotation_tick(n, x_un, y_un):
            """
            Performs the smallest move from the rotation
            :param n: node
            :param x_un: x_unit - amount to move along x-axis during single tick
            :param y_un: y_unit - amount to move along y-axis during single tick
            :return: returns nothing
            """
            self.canvas_now.delete(f'Line{hash(n)}')
            self.canvas_now.delete(f'Line{hash(n.parent)}')
            self.canvas_now.move(f'Node{hash(n)}', x_un, y_un)
            n.x += x_un
            n.y += y_un
            self.draw_line(self.canvas_now, n, n.right)
            self.draw_line(self.canvas_now, n, n.left)
            if n.parent is not None:
                self.draw_line(self.canvas_now, n.parent, n.parent.right)
                self.draw_line(self.canvas_now, n.parent, n.parent.left)
            self.canvas_now.tag_lower('Line')

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
                    rotation_tick(s, units[s][0], units[s][1])
                r.wait(self.animation_unit)
                tmp -= 1
