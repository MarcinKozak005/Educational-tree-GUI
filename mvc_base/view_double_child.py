from abc import ABC

from PIL import ImageTk, Image

import mvc_base.view as view


class DCView(view.View, ABC):
    def __init__(self, node_width, node_height, columns_to_skip):
        super().__init__(node_width, node_height, columns_to_skip)
        self.grey_circle = None

    def calculate_images(self):
        anti = Image.ANTIALIAS
        grey_circle = Image.open('./materials/grey_circle.png').resize((self.node_width, self.node_height), anti)
        self.grey_circle = ImageTk.PhotoImage(grey_circle)
