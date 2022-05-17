from PIL import ImageTk, Image

import avlt.avl_model as avlt
import mvc_base.model_double_child as mdc
import mvc_base.view_double_child as vdc
from core.constants import white, black, circle_node_text_modifier


class AVLView(vdc.DCView):

    def __init__(self, node_width, node_height, columns_to_skip):
        super().__init__(node_width, node_height, columns_to_skip)
        self.green_circle = None
        self.calculate_images()

    def calculate_images(self):
        super().calculate_images()
        anti = Image.ANTIALIAS
        green_circle = Image.open('./materials/green_circle.png').resize((self.node_width, self.node_height), anti)
        self.green_circle = ImageTk.PhotoImage(green_circle)

    def draw_tree(self, node, canvas, reload_images=False):
        if reload_images:
            self.calculate_images()
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

    def draw_object(self, obj, canvas=None):
        if canvas is None:
            canvas = self.canvas_now
        if type(obj) is avlt.AVLTNode:
            canvas.create_image(obj.x - self.node_width // 2, obj.y - self.node_height // 2,
                                image=self.green_circle, anchor='nw', tags=obj.tag())
            canvas.create_text(obj.x, obj.y, fill=white, text=obj.value, tags=obj.tag(),
                               font=('TkDefaultFont', int(self.node_width * circle_node_text_modifier), 'bold'))
            canvas.create_text(obj.x - self.node_width // 2, obj.y - self.node_height // 2,
                               fill=black, text=obj.height, tags=obj.tag(),
                               font=('TkDefaultFont', int((self.node_width - 4) * circle_node_text_modifier)))

    def draw_height_change(self, node):
        # Drawing node with new height
        self.erase(node.tag())
        self.draw_object(node)
        self.draw_exp_text(node, f'New height of node ({node.value}) is: {node.height}')
