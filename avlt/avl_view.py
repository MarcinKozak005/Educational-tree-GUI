import mvc_base.view as view


class AVLView(view.View):

    def __init__(self, node_width, node_height, columns_to_skip):
        super().__init__(node_width, node_height, columns_to_skip)

    def draw_tree(self, node, canvas):
        pass

    def draw_object_with_children_lines(self, obj, canvas):
        pass

    def draw_object(self, obj, canvas):
        pass
