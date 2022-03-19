import mvc_base.view as view
import avlt.avl_model as avlt
import mvc_base.model_double_child as mdc


class AVLView(view.View):

    def __init__(self, node_width, node_height, columns_to_skip):
        super().__init__(node_width, node_height, columns_to_skip)

    def draw_tree(self, node, canvas):
        if type(node) is not mdc.DCLeaf and node is not None:
            self.draw_object_with_children_lines(node, canvas)
            self.draw_tree(node.left, canvas)
            self.draw_tree(node.right, canvas)

    def draw_object_with_children_lines(self, obj, canvas):
        if type(obj.right) is not mdc.DCLeaf:
            self.draw_line(canvas, obj, obj.right)
        if type(obj.left) is not mdc.DCLeaf:
            self.draw_line(canvas, obj, obj.left)
        self.draw_object(obj, canvas)

    def draw_object(self, obj, canvas):
        if type(obj) is avlt.AVLTNode:
            canvas.create_oval(obj.x - self.node_width // 2, obj.y - self.node_height // 2,
                               obj.x + self.node_width // 2, obj.y + self.node_height // 2,
                               fill='green', tags=obj.tag())
            canvas.create_text(obj.x, obj.y, fill='white', text=obj.value, tags=obj.tag())
            canvas.create_text(obj.x-self.node_width//2, obj.y-self.node_height//2,
                               fill='black', text=obj.height, tags=obj.tag())
