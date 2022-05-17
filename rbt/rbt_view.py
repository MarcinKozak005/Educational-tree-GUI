from PIL import ImageTk, Image

import mvc_base.model_double_child as mdc
import mvc_base.view_double_child as vdc
import rbt.rbt_model as rbt
from core.constants import white, recolor_txt, black, circle_node_text_modifier


class RBTView(vdc.DCView):
    def __init__(self, node_width, node_height, columns_to_skip):
        super().__init__(node_width, node_height, columns_to_skip)
        self.black_circle = None
        self.red_circle = None
        self.calculate_images()

    def calculate_images(self):
        super().calculate_images()
        anti = Image.ANTIALIAS
        black_circle = Image.open('./materials/black_circle.png').resize((self.node_width, self.node_height), anti)
        red_circle = Image.open('./materials/red_circle.png').resize((self.node_width, self.node_height), anti)
        self.black_circle = ImageTk.PhotoImage(black_circle)
        self.red_circle = ImageTk.PhotoImage(red_circle)

    def draw_recolor_text(self, node, to_color):
        """
        Draws the recoloring info on the node
        :param node: the node to be recolored
        :param to_color: color to which the node is recolored
        :return: returns nothing
        """
        if type(node) is rbt.RBTNode:
            txt = self.canvas_now.create_text(node.x, node.y - self.node_height, fill=white,
                                              text=f'Change color to {to_color}', tags=recolor_txt)
            txt_bb = self.canvas_now.bbox(txt)
            if txt_bb[0] < 0:
                x_change = -txt_bb[0]
                self.canvas_now.move(txt, x_change, 0)
                txt_bb = (txt_bb[0] - x_change, txt_bb[1], txt_bb[2] - x_change, txt_bb[3])
            if txt_bb[2] - self.width > 0:
                x_change = -(txt_bb[2] - self.width)
                self.canvas_now.move(txt, x_change, 0)
                txt_bb = (txt_bb[0] + x_change, txt_bb[1], txt_bb[2] + x_change, txt_bb[3])
            txt_bg = self.canvas_now.create_rectangle(txt_bb, fill='grey', tags=recolor_txt)
            self.explanation.append(f'Change color of ({node.value}) to {to_color}')
            self.canvas_now.tag_lower(txt_bg, txt)

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
        if type(obj) is rbt.RBTNode:
            circle = self.black_circle if obj.color == black else self.red_circle
            canvas.create_image(obj.x - self.node_width // 2, obj.y - self.node_height // 2,
                                anchor='nw', image=circle, tags=obj.tag())
            canvas.create_text(obj.x, obj.y, fill=white, text=obj.value, tags=obj.tag(),
                               font=('TkDefaultFont', int(self.node_width * circle_node_text_modifier), 'bold'))
