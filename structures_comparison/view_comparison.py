import abc
import tkinter as tk

import customtkinter as ctk

import core.menu as m
import core.root as r
from core.constants import white, canvas_width_modifier, canvas_height_modifier

ctk.set_default_color_theme('green')
button_arguments = {'width': 20, 'height': 10, 'text_color_disabled': '#d1d1d1'}
btn_arg = {'width': 7, 'height': 7, 'text_color_disabled': '#d1d1d1'}  # for max_degree buttons


class ComparisonView:

    def __init__(self):
        self.width = int(r.frame.width * canvas_width_modifier)
        self.height = int(r.frame.height * canvas_height_modifier)
        self.canvas_top = None
        self.canvas_bottom = None
        self.info_label = None
        self.buttons = []
        self.top_canvas_label = None
        self.bottom_canvas_label = None
        self.controls_frame = None
        self.time_scale = None
        self.hold_animation = False
        self.pause_continue_button = None
        self.buttons_state = {}
        self.current_max_degree = None
        self.max_degree_buttons = []
        self.increase_size_button = None
        self.decrease_size_button = None
        self.size_value = 0

    @abc.abstractmethod
    def draw_tree(self, node, canvas, reload_images=False):
        # Draw both trees, call functions from respective views but canvases from this view
        pass

    def draw_exp_text(self, node, exp_str, above=True):
        # change draw_exp_text in all views to accept canvas
        """
        Draws explanation text above/below a given node
        :param node: node above/below which a exp_str will be drawn
        :param exp_str: string to draw
        :param above: if True -> exp_str will be above node, else below the node
        :return: returns nothing
        """
        pass

    def prepare_view(self):
        """
        Clears labels and canvas_bottom
        :return: returns nothing
        """
        self.info_label.config(text='')
        self.erase('all')

    def set_buttons(self, state):
        """
        Enables/Disable buttons
        :param state: if True -> enable buttons, else disable
        :return: returns nothing
        """
        for b in self.buttons:
            b.config(state=tk.NORMAL if state else tk.DISABLED)

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
        back_button = ctk.CTkButton(self.controls_frame, text='Back to menu', command=lambda: r.show_frame(m.frame),
                                    **button_arguments)
        self.info_label = tk.Label(self.controls_frame)

        # Putting on window
        input_field.grid(row=0, column=2)
        insert_button.grid(row=0, column=3, padx=5)
        delete_button.grid(row=0, column=4, padx=5)
        find_button.grid(row=0, column=5, padx=5)
        ctk.CTkLabel(self.controls_frame, text='Operations:').grid(row=0, column=6, padx=(5, 0))
        min_button.grid(row=0, column=7, padx=(5, 0))
        max_button.grid(row=0, column=8, padx=(5, 0))
        mean_button.grid(row=0, column=9, padx=(5, 0))
        median_button.grid(row=0, column=10, padx=(5, 0))

        clear_button.grid(row=0, column=11, padx=(5, 0))
        back_button.grid(row=0, column=17, padx=(40, 0))

        self.info_label.grid(row=1, column=0, columnspan=4, sticky='WE')
        self.controls_frame.pack()

        # Visualization frame
        visualization_frame = ctk.CTkFrame(frame)

        canvas_frame = ctk.CTkFrame(visualization_frame)
        self.top_canvas_label = ctk.CTkLabel(canvas_frame, text=f'State of the {text}:')
        self.canvas_top = ctk.CTkCanvas(canvas_frame, width=self.width, height=self.height, bg=white)
        self.bottom_canvas_label = ctk.CTkLabel(canvas_frame, text=f'State of the {text}:')
        self.canvas_bottom = ctk.CTkCanvas(canvas_frame, width=self.width, height=self.height, bg=white)
        self.top_canvas_label.pack(pady=(5, 0))
        self.canvas_top.pack()
        self.bottom_canvas_label.pack(pady=(5, 0))
        self.canvas_bottom.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        canvas_frame.grid(row=0, column=1)
        visualization_frame.pack(pady=(5, 0))

        self.buttons = [insert_button, delete_button, find_button, clear_button,
                        min_button, max_button, mean_button, median_button,
                        self.increase_size_button, self.decrease_size_button]

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

    def erase(self, tag):
        """
        Erases objects with 'tag" tag on the canvas_bottom
        :param tag: string representing the tag
        :return: returns nothing
        """
        self.canvas_top.delete(tag)
        self.canvas_bottom.delete(tag)
