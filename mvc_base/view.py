import abc
import tkinter as tk

import core.menu as m
import core.root as r


class View(abc.ABC):
    def __init__(self, node_width, node_height, columns_to_skip):
        self.explanation = Explanation()
        self.width = 1000
        self.height = 300
        self.y_space = 50
        self.y_above = 30
        self.node_width = node_width
        self.node_height = node_height
        self.long_animation_time = 150
        self.short_animation_time = 50
        self.animation_unit = 10
        self.layout = 'double'
        self.columns_to_skip = columns_to_skip
        self.canvas_now = None
        self.canvas_prev = None
        self.info_label = None
        self.explanation_label = None
        self.buttons = []
        self.prev_label = None
        self.now_label = None
        self.view_button = None
        self.explanation_frame = None
        self.controls_frame = None

    @abc.abstractmethod
    def draw_tree(self, node, canvas):
        pass

    @abc.abstractmethod
    def draw_object_with_children_lines(self, obj, canvas):
        pass

    @abc.abstractmethod
    def draw_object(self, obj, canvas):
        pass

    def animate(self, node, time=False):
        time = self.short_animation_time if time else self.long_animation_time
        if node is not None:
            successors = node.successors()
            units = {}
            tmp = time / self.animation_unit
            for s in successors:
                x_unit = (s.x_next - s.x) / tmp
                y_unit = (s.y_next - s.y) / tmp
                units[s] = (x_unit, y_unit)
            while tmp > 0:
                for s in successors:
                    s.tick(self, units[s][0], units[s][1])
                r.wait(self.animation_unit)
                tmp -= 1

    def draw_exp_text(self, node, exp_str, above=True):
        """
        Draws explanation text exp_str above/below a given node
        :param node: node above/below which a exp_str will be drawn
        :param exp_str: string to draw
        :param above: if True -> exp_str will be above node, else below the node
        :return: returns nothing
        """
        txt = self.canvas_now.create_text(node.x, node.y + (-1 if above else 1) * self.node_height,
                                          fill='white',
                                          text=exp_str,
                                          tags=r.exp_txt)
        txt_bg = self.canvas_now.create_rectangle(self.canvas_now.bbox(txt), fill="grey", tags=r.exp_txt)
        self.canvas_now.tag_lower(txt_bg)
        r.wait(self.long_animation_time)
        self.canvas_now.delete(r.exp_txt)
        self.explanation.append(exp_str)

    def move_object(self, obj, x1, y1, x2, y2, time=False):
        """
        Moves object obj from (x1,y1) to (x2,y2)
        :param obj: object to move identifier
        :param x1: initial x coordinate
        :param y1: initial y coordinate
        :param x2: final x coordinate
        :param y2: final y coordinate
        :return: returns nothing
        """
        time = self.short_animation_time if time else self.long_animation_time
        x_diff = x2 - x1
        y_diff = y2 - y1
        x_unit = x_diff / (time / self.animation_unit)
        y_unit = y_diff / (time / self.animation_unit)
        counter = time / self.animation_unit
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
        self.explanation_label.config(text=self.explanation.string, wraplength=350)
        self.explanation.reset()

    def set_buttons(self, value):
        """
        Enables/Disable buttons
        :param value: if True -> enable buttons, else disable
        :return: returns nothing
        """
        for b in self.buttons:
            b.config(state='normal' if value else 'disabled')

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

        self.controls_frame = tk.Frame(frame)
        insert_field = tk.Entry(self.controls_frame, width=7)
        insert_button = tk.Button(self.controls_frame, text='Add node',
                                  command=lambda: controller.perform(r.Action.insert, insert_field.get()))
        delete_field = tk.Entry(self.controls_frame, width=7)
        delete_button = tk.Button(self.controls_frame, text='Delete node',
                                  command=lambda: controller.perform(r.Action.delete, delete_field.get()))
        find_field = tk.Entry(self.controls_frame, width=7)
        find_button = tk.Button(self.controls_frame, text='Find node',
                                command=lambda: controller.perform(r.Action.search, find_field.get()))
        clear_button = tk.Button(self.controls_frame, text='Clear tree', command=lambda: controller.clear())
        self.view_button = tk.Button(self.controls_frame, text='Show previous state and explanation: ON',
                                     command=lambda: controller.change_layout())
        back_button = tk.Button(self.controls_frame, text='Back to menu', command=lambda: r.show_frame(m.frame))
        self.info_label = tk.Label(self.controls_frame)
        cts = self.columns_to_skip
        insert_field.grid(row=0, column=cts)
        insert_button.grid(row=0, column=cts + 1, padx=(0, 20))
        delete_field.grid(row=0, column=cts + 2)
        delete_button.grid(row=0, column=cts + 3, padx=(0, 20))
        find_field.grid(row=0, column=cts + 4)
        find_button.grid(row=0, column=cts + 5)
        self.view_button.grid(row=0, column=cts + 6, padx=(20, 20))
        clear_button.grid(row=0, column=cts + 7)
        back_button.grid(row=0, column=cts + 8, padx=(40, 0))
        self.info_label.grid(row=1, columnspan=6, sticky='WE')
        self.controls_frame.pack()

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

    def draw_line(self, canvas, node1, node2, from_side=tk.CENTER, to_side=tk.CENTER, fill='black'):
        """
        Draws a line between two nodes
        :param canvas: canvas to draw on
        :param node1: from-node
        :param node2: to-node
        :param from_side:
        :param to_side:
        :return: returns nothing
        """
        if node1 is not None and node2 is not None:
            from_mod = self.side_modifier(from_side)
            to_mod = self.side_modifier(to_side)
            try:
                canvas.create_line(node1.x + from_mod[0], node1.y + from_mod[1], node2.x + to_mod[0],
                                   node2.y + to_mod[1],
                                   fill=fill, tags=[f'Line{hash(node1)}', 'Line'])
            except AttributeError as e:
                print(e)


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
