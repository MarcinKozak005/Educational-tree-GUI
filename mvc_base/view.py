import abc
import tkinter as tk

import customtkinter as ctk

import core.menu as m
import core.root as r
from core.constants import hint_frame, exp_txt, white, black, animation_unit, canvas_width_modifier, \
    canvas_height_modifier, explanation_width_modifier, explanation_height_modifier

ctk.set_default_color_theme('green')
button_arguments = {'width': 20, 'height': 10, 'text_color_disabled': '#d1d1d1'}
btn_arg = {'width': 7, 'height': 7, 'text_color_disabled': '#d1d1d1'}  # for max_degree buttons


class View(abc.ABC):
    """View component of MVC design pattern"""

    def __init__(self, node_width, node_height, columns_to_skip):
        self.explanation = Explanation(self)
        self.hint_frame = HintFrame(self)
        self.width = int(r.frame.width * canvas_width_modifier)
        self.height = int(r.frame.height * canvas_height_modifier)
        self.y_space = 50
        self.y_above = 30
        self.node_width = node_width
        self.node_height = node_height
        self.long_animation_time = 2500
        self.short_animation_time = self.long_animation_time // 2
        self.layout = 'double'
        self.columns_to_skip = columns_to_skip
        self.canvas_now = None
        self.canvas_prev = None
        self.info_label = None
        self.explanation_text = None
        self.buttons = []
        self.prev_label = None
        self.now_label = None
        self.view_button = None
        self.explanation_frame = None
        self.controls_frame = None
        self.time_scale = None
        self.hold_animation = False
        self.pause_continue_button = None
        self.back_button = None
        self.forward_button = None
        self.buttons_state = {}
        self.current_max_degree = None
        self.max_degree_buttons = []
        self.increase_size_button = None
        self.decrease_size_button = None

    @abc.abstractmethod
    def draw_tree(self, node, canvas, reload_images=False):
        """
        Draws node and it's children and if applicable values
        :param node: node to be drawn
        :param canvas: canvas on which node will be drawn
        :param reload_images: if True the images of nodes/values will be reloaded
        :return: returns nothing
        """
        pass

    @abc.abstractmethod
    def draw_object_with_children_lines(self, obj, canvas):
        """
        Draws object (node or value) with children lines
        :param obj: object to be drawn
        :param canvas: canvas on which object will be drawn
        :return: returns nothing
        """
        pass

    @abc.abstractmethod
    def draw_object(self, obj, canvas):
        """
        Draws the object (node or value)
        :param obj: object to be drawn
        :param canvas: canvas on which the object will be drawn
        :return: returns nothing
        """
        pass

    @abc.abstractmethod
    def calculate_images(self):
        """
        Reloads necessary node images
        :return:
        """
        pass

    def animate(self, node, short_animation_time=False):
        """
        Performs the animation of elements (nodes and values)
        :param node: node which and whose successors should be animated
        :param short_animation_time: indicates which animation time should be used
        :return: returns nothing
        """
        time = self.short_animation_time if short_animation_time else self.long_animation_time
        if node is not None:
            successors = node.successors()
            units = {}
            counter = time / animation_unit
            for s in successors:
                x_unit = (s.x_next - s.x) / counter
                y_unit = (s.y_next - s.y) / counter
                units[s] = (x_unit, y_unit)
            # Skip waiting if units are too small
            if all(abs(x) < 0.00001 and abs(y) < 0.00001 for (x, y) in units.values()):
                return
            # Move each successor
            while counter > 0:
                for s in successors:
                    s.tick(self, units[s][0], units[s][1])
                r.wait(animation_unit)
                counter -= 1

    def draw_exp_text(self, node, exp_str, above=True):
        """
        Draws explanation text above/below a given node
        :param node: node above/below which a exp_str will be drawn
        :param exp_str: string to draw
        :param above: if True -> exp_str will be above node, else below the node
        :return: returns nothing
        """
        txt = self.canvas_now.create_text(node.x, node.y + (-1 if above else 1) * self.node_height, fill=white,
                                          text=exp_str, tags=exp_txt)
        txt_bb = self.canvas_now.bbox(txt)
        if txt_bb[0] < 0:
            x_change = -txt_bb[0]
            self.canvas_now.move(txt, x_change, 0)
            txt_bb = (txt_bb[0] - x_change, txt_bb[1], txt_bb[2] - x_change, txt_bb[3])
        if txt_bb[2] - self.width > 0:
            x_change = -(txt_bb[2] - self.width)
            self.canvas_now.move(txt, x_change, 0)
            txt_bb = (txt_bb[0] + x_change, txt_bb[1], txt_bb[2] + x_change, txt_bb[3])
        txt_background = self.canvas_now.create_rectangle(txt_bb, fill='grey', tags=exp_txt)
        self.canvas_now.tag_lower(txt_background, txt)
        r.wait(self.long_animation_time)
        self.erase(exp_txt)
        self.explanation.append(exp_str)

    def move_object(self, obj, x1, y1, x2, y2, short_animation_time=False):
        """
        Moves object obj by a distance (x2-x1, y2-y1)
        obj does not have to be in (x1,y1) to be moved
        :param short_animation_time: boolean, if True a shorter animation time will be used
        :param obj: object to move identifier
        :param x1: first x coordinate
        :param y1: first  y coordinate
        :param x2: second x coordinate
        :param y2: second y coordinate
        :return: returns nothing
        """
        time = self.short_animation_time if short_animation_time else self.long_animation_time
        x_diff = x2 - x1
        y_diff = y2 - y1
        x_unit = x_diff / (time / animation_unit)
        y_unit = y_diff / (time / animation_unit)
        counter = time / animation_unit
        # Move object
        while counter > 0:
            self.canvas_now.move(obj, x_unit, y_unit)
            r.wait(animation_unit)
            counter -= 1

    def clear(self):
        """
        Clears canvases and explanation label
        :return: returns nothing
        """
        self.canvas_prev.delete('all')
        self.erase('all')
        self.explanation_text.config(state=tk.NORMAL)
        self.explanation_text.delete(0.0, 'end')
        self.explanation_text.config(state=tk.DISABLED)

    def prepare_view(self):
        """
        Clears labels and canvas_now
        :return: returns nothing
        """
        self.info_label.config(text='')
        self.erase('all')
        self.explanation.reset()

    def set_buttons(self, state):
        """
        Enables/Disable buttons
        :param state: if True -> enable buttons, else disable
        :return: returns nothing
        """
        for b in self.buttons:
            b.config(state=tk.NORMAL if state else tk.DISABLED)

    def set_browsing_buttons(self, state):
        st = tk.NORMAL if state else tk.DISABLED
        self.forward_button.config(state=st)
        self.back_button.config(state=st)

    def check_browsing_buttons(self, pointer, length):
        """
        Disables/Enables history browsing buttons and operation buttons
        :param pointer: value of history_list in controller
        :param length: length of history_list in controller
        :return: returns nothing
        """
        self.back_button.config(state=tk.NORMAL if pointer > 0 else tk.DISABLED)
        if pointer < length - 1:
            self.forward_button.config(state=tk.NORMAL)
            self.set_buttons(False)
        else:
            self.forward_button.config(state=tk.DISABLED)
            self.set_buttons(True)
        self.check_max_degree_buttons()

    def check_max_degree_buttons(self):
        if self.max_degree_buttons:
            for b in self.max_degree_buttons:
                b.config(state=tk.DISABLED if int(b.text) == self.current_max_degree else tk.NORMAL)

    def create_GUI(self, controller, text):
        """
        Creates a GUI with buttons triggering model methods with the use of controller
        :param controller: controller to call model methods and to access the model
        :param text: String to be shown above all GUI elements
        :return: returns main tk.Frame with all GUI widgets
        """

        frame = tk.Frame(r.frame)

        main_subframe = ctk.CTkFrame(frame)
        ctk.CTkLabel(main_subframe, text=text, pady=7).pack()
        main_subframe.pack(fill='x')

        # Controls frame
        # First row of controls_frame
        self.controls_frame = tk.Frame(frame)
        input_field = ctk.CTkEntry(self.controls_frame, width=100, placeholder_text='Enter value')
        insert_button = ctk.CTkButton(self.controls_frame, text='Add node', **button_arguments,
                                      command=lambda: controller.perform(r.Action.insert, input_field.get()))
        delete_button = ctk.CTkButton(self.controls_frame, text='Delete node', **button_arguments,
                                      command=lambda: controller.perform(r.Action.delete, input_field.get()))
        find_button = ctk.CTkButton(self.controls_frame, text='Find node', **button_arguments,
                                    command=lambda: controller.perform(r.Action.search, input_field.get()))
        min_button = ctk.CTkButton(self.controls_frame, text='Min',
                                   command=lambda: controller.perform(r.Action.min, '0'), **button_arguments)
        max_button = ctk.CTkButton(self.controls_frame, text='Max',
                                   command=lambda: controller.perform(r.Action.max, '0'), **button_arguments)
        mean_button = ctk.CTkButton(self.controls_frame, text='Mean', **button_arguments,
                                    command=lambda: controller.perform(r.Action.mean, '0'))
        median_button = ctk.CTkButton(self.controls_frame, text='Median', **button_arguments,
                                      command=lambda: controller.perform(r.Action.median, '0'))

        clear_button = ctk.CTkButton(self.controls_frame, text='Clear tree', command=lambda: controller.clear(),
                                     **button_arguments)
        self.view_button = ctk.CTkButton(self.controls_frame, text='Show previous state and explanation: ON',
                                         command=lambda: controller.change_layout(), **button_arguments)
        back_button = ctk.CTkButton(self.controls_frame, text='Back to menu', command=lambda: r.show_frame(m.frame),
                                    **button_arguments)

        # Second row of controls_frame
        def pause_continue_animation():
            if self.hold_animation:
                # Load buttons state
                for b in self.buttons_state.keys():
                    b.config(state=self.buttons_state[b])
                # Change GUI
                self.pause_continue_button.config(text='Pause')
                self.info_label.config(text='', fg='black', font='TkDefaultFont')
                self.hold_animation = False
            elif not self.hold_animation:
                # Save buttons state
                for b in self.buttons:
                    self.buttons_state[b] = b.state
                    self.buttons_state[self.back_button] = self.back_button.state
                    self.buttons_state[self.forward_button] = self.forward_button.state
                # Change GUI and hold animation
                self.set_buttons(False)
                self.pause_continue_button.config(text='Continue')
                self.back_button.config(state=tk.DISABLED)
                self.forward_button.config(state=tk.DISABLED)
                self.info_label.config(text=f'Animation paused! Press \'{self.pause_continue_button.text}\' to '
                                            f'continue', fg='red')
                self.hold_animation = True
                while self.hold_animation:
                    r.wait(10)

        def selector_change(new_value):
            self.long_animation_time = int(new_value)
            self.short_animation_time = int(new_value) // 2

        self.info_label = tk.Label(self.controls_frame)
        self.back_button = ctk.CTkButton(self.controls_frame, text='<<<', command=controller.back, **button_arguments)
        self.forward_button = ctk.CTkButton(self.controls_frame, text='>>>', command=controller.forward,
                                            **button_arguments)
        self.pause_continue_button = ctk.CTkButton(self.controls_frame, text='Pause', command=pause_continue_animation,
                                                   **button_arguments)
        self.time_scale = ctk.CTkSlider(self.controls_frame, from_=5000, to=50, width=155, command=selector_change)
        self.time_scale.set(self.long_animation_time)

        # Putting on window
        cts = self.columns_to_skip
        input_field.grid(row=0, column=cts)
        insert_button.grid(row=0, column=cts + 1, padx=5)
        delete_button.grid(row=0, column=cts + 2, padx=5)
        find_button.grid(row=0, column=cts + 3, padx=5)
        ctk.CTkLabel(self.controls_frame, text='Operations:').grid(row=0, column=cts + 4, padx=(5, 0))
        min_button.grid(row=0, column=cts + 5, padx=(5, 0))
        max_button.grid(row=0, column=cts + 6, padx=(5, 0))
        mean_button.grid(row=0, column=cts + 7, padx=(5, 0))
        median_button.grid(row=0, column=cts + 8, padx=(5, 0))

        #
        def decrease():
            self.node_width -= 6
            self.node_height -= 6
            self.y_space -= 12
            self.y_above -= 7
            self.erase('all')
            controller.tree.update_positions(True)
            self.draw_tree(controller.tree.root, self.canvas_now, True)

        def increase():
            self.node_width += 6
            self.node_height += 6
            self.y_space += 12
            self.y_above += 7
            self.erase('all')
            controller.tree.update_positions(True)
            self.draw_tree(controller.tree.root, self.canvas_now, True)

        self.increase_size_button = ctk.CTkButton(self.controls_frame, text='-', command=decrease, **button_arguments)
        self.decrease_size_button = ctk.CTkButton(self.controls_frame, text='+', command=increase, **button_arguments)
        self.increase_size_button.grid(row=1, column=cts + 7, padx=(5, 0))
        self.decrease_size_button.grid(row=1, column=cts + 8, padx=(5, 0))
        #

        clear_button.grid(row=0, column=cts + 9, padx=(5, 0))
        self.view_button.grid(row=0, column=cts + 10, columnspan=5, padx=(20, 20))
        back_button.grid(row=0, column=cts + 15, padx=(40, 0))

        self.info_label.grid(row=1, column=0, columnspan=4, sticky='WE')
        ctk.CTkLabel(self.controls_frame, text='Animation:').grid(row=1, column=cts + 4, padx=(5, 0))
        self.back_button.grid(row=1, column=cts + 5)
        self.forward_button.grid(row=1, column=cts + 6)
        self.check_browsing_buttons(controller.history.pointer, len(controller.history.history_list))
        self.pause_continue_button.grid(row=1, column=cts + 9)
        ctk.CTkLabel(self.controls_frame, text='Anim. speed:').grid(row=1, column=cts + 10)
        self.time_scale.grid(row=1, column=cts + 11, columnspan=3)

        self.controls_frame.pack()

        # Visualization frame
        visualization_frame = ctk.CTkFrame(frame)
        self.explanation_frame = ctk.CTkFrame(visualization_frame)
        explanation_title_label = ctk.CTkLabel(self.explanation_frame, text='')
        explanation_label = tk.Label(self.explanation_frame, text='')
        self.explanation_text = tk.Text(explanation_label,
                                        width=int(r.frame.width * explanation_width_modifier),
                                        height=int(r.frame.height * explanation_height_modifier),
                                        bg=frame.cget('bg'), font='TkDefaultFont')
        explanation_scrollbar = tk.Scrollbar(explanation_label, command=self.explanation_text.yview, width=5)
        self.explanation_text.config(yscrollcommand=explanation_scrollbar.set, state=tk.DISABLED)
        explanation_title_label.config(text=f'{text} explanation')
        explanation_title_label.grid(row=0, column=0)
        explanation_label.grid(row=1, column=0)
        self.explanation_text.grid(row=1, column=1)
        explanation_scrollbar.grid(row=1, column=0, sticky=tk.NSEW)
        self.explanation_frame.grid(row=0, column=0, sticky='NS')

        canvas_frame = ctk.CTkFrame(visualization_frame)
        self.prev_label = ctk.CTkLabel(canvas_frame, text=f'Previous state of the {text}:')
        self.canvas_prev = ctk.CTkCanvas(canvas_frame, width=self.width, height=self.height, bg=white)
        self.now_label = ctk.CTkLabel(canvas_frame, text=f'Current state of the {text}:')
        self.canvas_now = ctk.CTkCanvas(canvas_frame, width=self.width, height=self.height, bg=white)
        self.prev_label.pack(pady=(5, 0))
        self.canvas_prev.pack()
        self.now_label.pack(pady=(5, 0))
        self.canvas_now.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        canvas_frame.grid(row=0, column=1)
        visualization_frame.pack(pady=(5, 0))

        self.buttons = [insert_button, delete_button, find_button, clear_button, self.view_button,
                        min_button, max_button, mean_button, median_button]

        return frame

    def add_max_degree_change_to_GUI(self, controller):
        def selector_change(new_value):
            if self.current_max_degree != new_value:
                self.current_max_degree = new_value
                controller.clear()
                controller.tree = type(controller.tree)(self, new_value)
                for b in self.max_degree_buttons:
                    b.config(state=tk.DISABLED if int(b.text) == new_value else tk.NORMAL)

        degree_btn_frame = tk.Frame(self.controls_frame)
        self.max_degree_buttons.append(ctk.CTkButton(degree_btn_frame, text='3',
                                                     command=lambda: selector_change(3), **btn_arg))
        self.max_degree_buttons.append(ctk.CTkButton(degree_btn_frame, text='4',
                                                     command=lambda: selector_change(4), **btn_arg))
        self.max_degree_buttons.append(ctk.CTkButton(degree_btn_frame, text='5',
                                                     command=lambda: selector_change(5), **btn_arg))
        self.max_degree_buttons.append(ctk.CTkButton(degree_btn_frame, text='6',
                                                     command=lambda: selector_change(6), **btn_arg))
        tk.Label(self.controls_frame, text='Max graph degree:').grid(row=0, column=0)
        degree_btn_frame.grid(row=0, column=1)
        for btn in self.max_degree_buttons:
            btn.grid(row=0, column=self.max_degree_buttons.index(btn),
                     padx=(0, 10 if btn is self.max_degree_buttons[-1] else 1))
        self.max_degree_buttons[0].config(state=tk.DISABLED)
        self.buttons.extend(self.max_degree_buttons)

    def calculate_anchor(self, anchor):
        """
        Translates tkinter anchor to x_mod and y_mod which represent given anchor
        :param anchor: tkinter anchor
        :return: tuple (x_mod,y_mod) of values how much x and y coordinate of node should be changed
        to represent the anchor
        """
        if anchor == tk.NE:
            sides = [tk.N, tk.E]
        elif anchor == tk.SE:
            sides = [tk.S, tk.E]
        elif anchor == tk.SW:
            sides = [tk.S, tk.W]
        elif anchor == tk.NW:
            sides = [tk.N, tk.W]
        else:
            sides = [anchor]

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

    def draw_line(self, canvas, node1, node2, from_side=tk.CENTER, to_side=tk.CENTER, fill=black):
        """
        Draws a line between two nodes
        :param canvas: canvas to draw on
        :param node1: from-node
        :param node2: to-node
        :param from_side: tkinter anchor. Indicates from which side of node1 the line starts
        :param to_side: tkinter anchor. Indicates to which side of node2 the line goes
        :param fill: color of the line
        :return: returns nothing
        """
        if node1 is not None and node2 is not None:
            from_mod = self.calculate_anchor(from_side)
            to_mod = self.calculate_anchor(to_side)
            try:
                canvas.create_line(node1.x + from_mod[0], node1.y + from_mod[1],
                                   node2.x + to_mod[0], node2.y + to_mod[1],
                                   fill=fill, tags=[f'Line{hash(node1)}', 'Line'], width=2 if fill == black else 1)
                canvas.tag_lower('Line')
            except AttributeError as e:
                print(e)

    def erase(self, tag):
        """
        Erases objects with 'tag" tag on the canvas_now
        :param tag: string representing the tag
        :return: returns nothing
        """
        self.canvas_now.delete(tag)


class HintFrame:
    """
    Class to operate on hint frame, which shows some operations such as search_value on the tree
    """

    def __init__(self, view):
        self.view = view
        self.x = 0
        self.y = 0

    def draw(self, x=None, y=None):
        """Draws hint frame in the given location"""
        x = x if x else self.x
        y = y if y else self.y
        self.x = x
        self.y = y
        self.view.canvas_now.create_rectangle(x - self.view.node_width // 2, y - self.view.node_height // 2,
                                              x + self.view.node_width // 2, y + self.view.node_height // 2,
                                              outline='red', tags=hint_frame)

    def move(self, x, y, time=False):
        """Moves the hint frame and updates it's coordinates"""
        self.view.move_object(hint_frame, self.x, self.y, x, y, time)
        self.x = x
        self.y = y


class Explanation:
    """Class responsible for showing the explanations next to the canvases"""

    def __init__(self, view):
        self.view = view
        self.line = 1

    def append(self, text):
        """
        Appends text with line number to string
        :param text: text to be appended
        :return: returns nothing
        """
        string = f'{self.line}) {text}\n'
        self.view.explanation_text.config(state=tk.NORMAL)
        self.view.explanation_text.insert('end', string)
        self.view.explanation_text.config(state=tk.DISABLED)
        self.line += 1

    def reset(self):
        """
        Resets all values
        :return: returns nothing
        """
        self.line = 1
