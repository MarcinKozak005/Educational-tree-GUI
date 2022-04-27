from abc import ABC

from PIL import ImageTk, Image

import mvc_base.view as view


class MCView(view.View, ABC):
    def __init__(self, node_width, node_height, columns_to_skip):
        super().__init__(node_width, node_height, columns_to_skip)
        self.green_square = None
        self.grey_square = None

    def calculate_images(self):
        anti = Image.ANTIALIAS
        grey_square = Image.open('./materials/grey_square.png').resize((self.node_width, self.node_height), anti)
        green_square = Image.open('./materials/green_square.png').resize((self.node_width, self.node_height), anti)
        self.grey_square = ImageTk.PhotoImage(grey_square)
        self.green_square = ImageTk.PhotoImage(green_square)
