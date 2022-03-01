import mvc_base.view as view
import rbt.rbt_model as rbt


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
            txt_bg = self.canvas_now.create_rectangle(self.canvas_now.bbox(txt), fill='grey', tags='recolor_txt')
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
            self.draw_object_with_children_lines(node, canvas)
            self.draw_tree(node.left, canvas)
            self.draw_tree(node.right, canvas)

    def draw_object_with_children_lines(self, obj, canvas):
        """
        Draws node with children lines
        :param node: node to draw
        :param canvas: canvas on which node will be drawn
        :return: returns nothing
        """
        if type(obj.right) is not rbt.RBTLeaf:
            self.draw_line(canvas, obj, obj.right)
        if type(obj.left) is not rbt.RBTLeaf:
            self.draw_line(canvas, obj, obj.left)
        self.draw_object(obj, canvas)

    def draw_object(self, node, canvas):
        """
        Draws the node
        :param node: node to be drawn
        :param canvas: canvas on which the node will be drawn
        :return: returns nothing
        """
        if type(node) is rbt.RBTNode:
            canvas.create_oval(node.x - self.node_width // 2, node.y - self.node_height // 2,
                               node.x + self.node_width // 2,
                               node.y + self.node_height // 2, fill=node.color, tags=node.tag())
            canvas.create_text(node.x, node.y, fill='white', text=node.value, tags=node.tag())