import tkinter as tk
import core.menu as m
import core.root as r
import redblack_tree.rbt_model as rbt


class View:
    def __init__(self, node_size):
        self.explanation = Explanation()
        self.width = 1000
        self.height = 300
        self.y_space = 50
        self.y_above = 30
        self.node_size = node_size
        self.half_node_size = node_size / 2
        self.animation_time = 150
        self.animation_unit = 10
        self.layout = 'double'
        self.canvas_now = None
        self.canvas_prev = None
        self.info_label = None
        self.explanation_label = None
        self.buttons = []
        self.prev_label = None
        self.explanation_frame = None
        self.now_label = None
        self.view_button = None

    def create_GUI(self, controller):
        """
        Creates a GUI with buttons triggering model methods with the use of controller
        :param controller: controller to call model methods and to access the model
        :return: returns main tk.Frame with all GUI widgets
        """

        frame = tk.Frame(r.frame)

        main_subframe = tk.Frame(frame)
        tk.Label(main_subframe, text='RedBlack Tree', bg='red', height=2).pack(fill='x')
        main_subframe.pack(fill='x')

        controls_frame = tk.Frame(frame)
        insert_field = tk.Entry(controls_frame)
        insert_button = tk.Button(controls_frame, text='Add node',
                                  command=lambda: controller.perform(r.Action.insert, insert_field.get()))
        delete_field = tk.Entry(controls_frame)
        delete_button = tk.Button(controls_frame, text='Delete node',
                                  command=lambda: controller.perform(r.Action.delete, delete_field.get()))
        find_field = tk.Entry(controls_frame)
        find_button = tk.Button(controls_frame, text='Find node',
                                command=lambda: controller.perform(r.Action.search, find_field.get()))
        clear_button = tk.Button(controls_frame, text='Clear tree', command=lambda: controller.clear())
        self.view_button = tk.Button(controls_frame, text='Show previous state and explanation: ON',
                                     command=lambda: controller.change_layout())
        back_button = tk.Button(controls_frame, text='Back to menu', command=lambda: r.show_frame(m.frame))
        self.info_label = tk.Label(controls_frame)
        insert_field.grid(row=0, column=0)
        insert_button.grid(row=0, column=1, padx=(0, 20))
        delete_field.grid(row=0, column=2)
        delete_button.grid(row=0, column=3, padx=(0, 20))
        find_field.grid(row=0, column=4)
        find_button.grid(row=0, column=5)
        self.view_button.grid(row=0, column=6, padx=(20, 20))
        clear_button.grid(row=0, column=7)
        back_button.grid(row=0, column=8, padx=(40, 0))
        self.info_label.grid(row=1, columnspan=6, sticky='WE')
        controls_frame.pack()

        visualization_frame = tk.Frame(frame)
        self.explanation_frame = tk.Frame(visualization_frame)
        explanation_title_lab = tk.Label(self.explanation_frame)
        self.explanation_label = tk.Label(self.explanation_frame)
        self.explanation_label.config(text='', justify=tk.LEFT, width=50, anchor=tk.W)
        explanation_title_lab.config(text='Explanation', font=15)
        explanation_title_lab.pack()
        self.explanation_label.pack()
        self.explanation_frame.grid(row=0, column=0, sticky='NS')

        canvas_frame = tk.Frame(visualization_frame)
        self.prev_label = tk.Label(canvas_frame, text='Previous state of the tree:')
        self.canvas_prev = tk.Canvas(canvas_frame, width=self.width, height=self.height, bg='white')
        self.now_label = tk.Label(canvas_frame, text='Current state of the tree:')
        self.canvas_now = tk.Canvas(canvas_frame, width=self.width, height=self.height, bg='white')
        self.prev_label.pack(pady=(5, 0))
        self.canvas_prev.pack()
        self.now_label.pack(pady=(5, 0))
        self.canvas_now.pack()
        canvas_frame.grid(row=0, column=1)
        visualization_frame.pack()

        self.buttons = [insert_button, delete_button, find_button, clear_button, self.view_button]

        return frame

    def draw_exp_text(self, node, exp_str, above=True):
        """
        Draws explanation text exp_str above/below a given node
        :param node: node above/below which a exp_str will be drawn
        :param exp_str: string to draw
        :param above: if True -> exp_str will be above node, else below the node
        :return: returns nothing
        """
        txt = self.canvas_now.create_text(node.x, node.y + (-1 if above else 1) * self.node_size,
                                          fill='white',
                                          text=exp_str,
                                          tags='exp_txt')
        txt_bg = self.canvas_now.create_rectangle(self.canvas_now.bbox(txt), fill="grey", tags='exp_txt')
        self.canvas_now.tag_lower(txt_bg)
        r.wait(self.animation_time)
        self.canvas_now.delete('exp_txt')
        self.explanation.append(exp_str)

    def draw_recolor_text(self, node, to_color):
        """
        Draws the recoloring info on the node
        :param node: the node to be recolored
        :param to_color: color to which the node is recolored
        :return: returns nothing
        """
        if type(node) is rbt.RBTree.RBNode:
            txt = self.canvas_now.create_text(node.x, node.y - self.node_size,
                                              fill='white',
                                              text=f'Change color to {to_color}',
                                              tags='recolor_txt')
            txt_bg = self.canvas_now.create_rectangle(self.canvas_now.bbox(txt), fill="grey", tags='recolor_txt')
            self.explanation.append(f'Change color of {node.value} to {to_color}')
            self.canvas_now.tag_lower(txt_bg)

    def draw_rb_tree(self, node, canvas):
        """
        Draws node and it's left/right subtrees
        :param node: node to draw
        :param canvas: canvas on which node will be drawn
        :return: returns nothing
        """
        if type(node) is not rbt.RBTree.RBLeaf and node is not None:
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
        if type(node) is not rbt.RBTree.RBLeaf:
            if type(node.right) is not rbt.RBTree.RBLeaf:
                self.draw_line(canvas, node, node.right)
            if type(node.left) is not rbt.RBTree.RBLeaf:
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
        if node1 is not None and node2 is not None and type(node1) is not rbt.RBTree.RBLeaf \
                and type(node2) is not rbt.RBTree.RBLeaf:
            canvas.create_line(node1.x, node1.y, node2.x, node2.y, fill='black',
                               tags=[f'Line{hash(node1)}', 'Line'])

    def draw_node(self, node, canvas):
        """
        Draws the node
        :param node: node to be drawn
        :param canvas: canvas on which the node will be drawn
        :return: returns nothing
        """
        if type(node) is rbt.RBTree.RBNode:
            canvas.create_oval(node.x - self.half_node_size, node.y - self.half_node_size, node.x + self.half_node_size,
                               node.y + self.half_node_size, fill=node.color, tags=f'Node{hash(node)}')
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

    def move_object(self, obj, x1, y1, x2, y2):
        """
        Moves object obj from (x1,y1) to (x2,y2)
        :param obj: object to move identifier
        :param x1: initial x coordinate
        :param y1: initial y coordinate
        :param x2: final x coordinate
        :param y2: final y coordinate
        :return: returns nothing
        """
        x_diff = x2 - x1
        y_diff = y2 - y1
        x_unit = x_diff / (self.animation_time / self.animation_unit)
        y_unit = y_diff / (self.animation_time / self.animation_unit)
        counter = self.animation_time / self.animation_unit
        while counter > 0:
            self.canvas_now.move(obj, x_unit, y_unit)
            r.wait(self.animation_unit)
            counter -= 1

    def clear(self):
        """
        Clears canvases and explanation label
        :return: returns nothing
        """
        self.canvas_prev.delete('all')
        self.canvas_now.delete('all')
        self.explanation_label.config(text='')

    def prepare_view(self):
        """
        Clears labels and canvas_now
        :return: returns nothing
        """
        self.info_label.config(text='')
        self.canvas_now.delete('all')
        self.explanation_label.config(text=self.explanation.string, wraplength=300)
        self.explanation.reset()

    def set_buttons(self, value):
        """
        Enables/Disable buttons
        :param value: if True -> enable buttons, else disable
        :return: returns nothing
        """
        for b in self.buttons:
            b.config(state='normal' if value else 'disabled')


class Explanation:

    def __init__(self):
        self.string = ''
        self.line = 1

    def append(self, text):
        """
        Appends text with line number to string
        :param text: text to be appended
        :return: returns nothing
        """
        self.string += f'[{self.line}] {text}\n'
        self.line += 1

    def reset(self):
        """
        Resets all values
        :return: returns nothing
        """
        self.string = ''
        self.line = 1
