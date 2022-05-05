import tkinter as tk

import customtkinter as ctk

import asa_graph.asag_model as asa
import asa_graph.asag_view as asav
import avbpt.avbpt_model as avbpt
import avbpt.avbpt_view as avbptv
import avbt.avbt_model as avbt
import avbt.avbt_view as avbtv
import avlt.avl_model as avl
import avlt.avl_view as avlv
import bpt.bpt_model as bpt
import bpt.bpt_view as bptv
import bt.bt_model as bt
import bt.bt_view as btv
import core.menu as m
import core.root as r
import rbt.rbt_model as rbt
import rbt.rbt_view as rbtv
from core.constants import white, canvas_width_modifier, canvas_height_modifier

button_arguments = {'width': 20, 'height': 10, 'text_color_disabled': '#d1d1d1'}
comparison_buttons_argument = {'width': 75, 'height': 10, 'text_color_disabled': '#d1d1d1'}
btn_arg = {'width': 7, 'height': 7, 'text_color_disabled': '#d1d1d1'}  # for max_degree buttons


class ComparisonView:

    def __init__(self):
        self.width = int(r.frame.width * canvas_width_modifier)
        self.height = int(r.frame.height * canvas_height_modifier)
        self.info_label = None
        self.buttons = []
        self.controls_frame = None
        self.time_scale = None
        self.buttons_state = {}
        self.increase_size_button = None
        self.decrease_size_button = None
        self.size_value = 0
        self.back_button = None
        self.forward_button = None
        # Top
        self.canvas_top = None
        self.top_canvas_label = None
        self.top_btns_degree = []
        self.top_max_degree = 3
        # Bottom
        self.canvas_bottom = None
        self.bottom_canvas_label = None
        self.bottom_btns_degree = []
        self.bottom_max_degree = 3

    def set_buttons(self, state):
        """
        Enables/Disable buttons
        :param state: if True -> enable buttons, else disable
        :return: returns nothing
        """
        for b in self.buttons:
            b.config(state=tk.NORMAL if state else tk.DISABLED)

    def set_buttons_degree(self, mode, state, degree=None):
        """
        Enables/Disable max-degree buttons
        :param mode: Mode.up or Mode.down. Distinguished which buttons should be affected
        :param state: True -> enable, False -> disable
        :param degree: int; button with that degree number should be disabled no matter the given state
        :return:
        """
        buttons_tab = self.top_btns_degree if mode == r.Mode.up else self.bottom_btns_degree
        for b in buttons_tab:
            b.config(state=tk.NORMAL if state else tk.DISABLED)
            if int(b.text) == degree:
                b.config(state=tk.DISABLED)

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
        else:
            self.forward_button.config(state=tk.DISABLED)

    def set_browsing_buttons(self, state):
        st = tk.NORMAL if state else tk.DISABLED
        self.forward_button.config(state=st)
        self.back_button.config(state=st)

    def check_size_buttons(self):
        if self.size_value <= 0:
            self.decrease_size_button.config(state=tk.DISABLED)
        elif self.size_value >= 4:
            self.increase_size_button.config(state=tk.DISABLED)
        else:
            self.decrease_size_button.config(state=tk.NORMAL)
            self.increase_size_button.config(state=tk.NORMAL)

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

        # Second row
        def selector_change(new_value):
            controller.top_tree.view.long_animation_time = int(new_value)
            controller.bottom_tree.view.long_animation_time = int(new_value)
            controller.top_tree.view.short_animation_time = int(new_value) // 2
            controller.bottom_tree.view.short_animation_time = int(new_value) // 2

        self.info_label = tk.Label(self.controls_frame)
        self.back_button = ctk.CTkButton(self.controls_frame, text='<<<', command=controller.back, **button_arguments)
        self.forward_button = ctk.CTkButton(self.controls_frame, text='>>>', command=controller.forward,
                                            **button_arguments)

        def decrease():
            self.increase_size_button.config(state=tk.NORMAL)
            self.size_value -= 1
            controller.top_tree.view.node_width -= 6
            controller.bottom_tree.view.node_width -= 6
            controller.top_tree.view.node_height -= 6
            controller.bottom_tree.view.node_height -= 6
            controller.top_tree.view.y_space -= 12
            controller.bottom_tree.view.y_space -= 12
            controller.top_tree.view.y_above -= 7
            controller.bottom_tree.view.y_above -= 7
            self.erase()
            controller.top_tree.update_positions(True)
            controller.bottom_tree.update_positions(True)
            controller.top_tree.view.draw_tree(controller.top_tree.root, self.canvas_top, True)
            controller.bottom_tree.view.draw_tree(controller.bottom_tree.root, self.canvas_bottom, True)
            self.check_size_buttons()

        def increase():
            self.decrease_size_button.config(state=tk.NORMAL)
            self.size_value += 1
            controller.top_tree.view.node_width += 6
            controller.bottom_tree.view.node_width += 6
            controller.top_tree.view.node_height += 6
            controller.bottom_tree.view.node_height += 6
            controller.top_tree.view.y_space += 12
            controller.bottom_tree.view.y_space += 12
            controller.top_tree.view.y_above += 7
            controller.bottom_tree.view.y_above += 7
            self.erase()
            controller.top_tree.update_positions(True)
            controller.bottom_tree.update_positions(True)
            controller.top_tree.view.draw_tree(controller.top_tree.root, self.canvas_top, True)
            controller.bottom_tree.view.draw_tree(controller.bottom_tree.root, self.canvas_bottom, True)
            self.check_size_buttons()

        size_frame = tk.Frame(self.controls_frame)
        self.decrease_size_button = ctk.CTkButton(size_frame, text='-', command=decrease, **button_arguments)
        self.increase_size_button = ctk.CTkButton(size_frame, text='+', command=increase, **button_arguments)
        self.check_size_buttons()

        self.time_scale = ctk.CTkSlider(self.controls_frame, from_=5000, to=50, width=155, command=selector_change)
        self.time_scale.set(2500)

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
        ctk.CTkLabel(self.controls_frame, text='Animation:').grid(row=1, column=6, padx=(5, 0))
        self.back_button.grid(row=1, column=7)
        self.forward_button.grid(row=1, column=8)
        self.controls_frame.pack()

        # Size frame
        self.decrease_size_button.grid(row=0, column=0, padx=(5, 0))
        self.increase_size_button.grid(row=0, column=1, padx=(5, 0))
        tk.Label(self.controls_frame, text='Size:').grid(row=1, column=9, sticky=tk.E)
        size_frame.grid(row=1, column=10)
        # Size frame end
        ctk.CTkLabel(self.controls_frame, text='Anim. speed:').grid(row=1, column=11)
        self.time_scale.grid(row=1, column=12, columnspan=3)

        # Visualization frame
        visualization_frame = ctk.CTkFrame(frame)
        comparison_frame = ctk.CTkFrame(visualization_frame)
        top_comparison_frame = tk.Frame(comparison_frame, height=self.height + 35, bg='#d1d1d1')
        top_comparison_frame.grid_propagate(0)
        bottom_comparison_frame = tk.Frame(comparison_frame, bg='#d1d1d1')

        # Short versions
        bcf = bottom_comparison_frame
        tcf = top_comparison_frame
        c = controller
        st = r.Structure
        up = r.Mode.up
        down = r.Mode.down
        cba = comparison_buttons_argument

        def selector_change(num, top):
            if top:
                if num != controller.top_tree_degree:
                    controller.top_tree_degree = num
                    self.top_max_degree = num
                    controller.clear()
                    controller.top_tree = type(controller.top_tree)(controller.top_tree.view, num)
                    controller.check_buttons()
                    self.top_canvas_label.config(text=f'{controller.top_structure.value} '
                                                      f'[degree: {controller.top_tree_degree}]')
            else:
                if num != controller.bottom_tree_degree:
                    controller.bottom_tree_degree = num
                    self.bottom_max_degree = num
                    controller.clear()
                    controller.bottom_tree = type(controller.bottom_tree)(controller.bottom_tree.view, num)
                    controller.check_buttons()
                    self.bottom_canvas_label.config(
                        text=f'{controller.bottom_structure.value} [degree: {controller.bottom_tree_degree}]')

        top_btns = [
            ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.RBT, up), text='Red-black', **cba),
            ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.AVL, up), text='AVL', **cba),
            ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.BT, up), text='B-', **cba),
            ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.BPT, up), text='B+', **cba),
            ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.AVBT, up), text='AVB-', **cba),
            ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.AVBPT, up), text='AVB+', **cba),
            ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.ASA, up), text='ASA', **cba)]
        degree_btn_frame1 = tk.Frame(tcf, bg='#d1d1d1')
        self.top_btns_degree = [
            ctk.CTkButton(degree_btn_frame1, text='3', command=lambda: selector_change(3, True), **btn_arg),
            ctk.CTkButton(degree_btn_frame1, text='4', command=lambda: selector_change(4, True), **btn_arg),
            ctk.CTkButton(degree_btn_frame1, text='5', command=lambda: selector_change(5, True), **btn_arg),
            ctk.CTkButton(degree_btn_frame1, text='6', command=lambda: selector_change(6, True), **btn_arg)
        ]

        bottom_btns = [
            ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.RBT, down), text='Red-black', **cba),
            ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.AVL, down), text='AVL', **cba),
            ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.BT, down), text='B-', **cba),
            ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.BPT, down), text='B+', **cba),
            ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.AVBT, down), text='AVB-', **cba),
            ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.AVBPT, down), text='AVB+', **cba),
            ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.ASA, down), text='ASA', **cba)]
        degree_btn_frame2 = tk.Frame(bcf, bg='#d1d1d1')
        self.bottom_btns_degree = [
            ctk.CTkButton(degree_btn_frame2, text='3', command=lambda: selector_change(3, False), **btn_arg),
            ctk.CTkButton(degree_btn_frame2, text='4', command=lambda: selector_change(4, False), **btn_arg),
            ctk.CTkButton(degree_btn_frame2, text='5', command=lambda: selector_change(5, False), **btn_arg),
            ctk.CTkButton(degree_btn_frame2, text='6', command=lambda: selector_change(6, False), **btn_arg)
        ]

        ctk.CTkLabel(top_comparison_frame, text='Top structure',
                     text_font=('TkDefaultFont', 10, 'bold')).grid(row=0, column=0)
        for i in range(0, len(top_btns)):
            top_btns[i].grid(row=i + 1, column=0, pady=(0, 2))
        degree_btn_frame1.grid(row=8, column=0)
        ctk.CTkLabel(degree_btn_frame1, text='Max graph degree:').grid(row=0, column=0, columnspan=4)
        for i in range(0, len(self.top_btns_degree)):
            self.top_btns_degree[i].grid(row=1, column=i)
        top_comparison_frame.grid(row=0, column=0, sticky=tk.NSEW)

        ctk.CTkLabel(bottom_comparison_frame, text='Bottom structure',
                     text_font=('TkDefaultFont', 10, 'bold')).grid(row=0, column=0)
        for i in range(0, len(bottom_btns)):
            bottom_btns[i].grid(row=i + 1, column=0, pady=(0, 2))
        degree_btn_frame2.grid(row=8, column=0)
        ctk.CTkLabel(degree_btn_frame2, text='Max graph degree:').grid(row=0, column=0, columnspan=4)
        for i in range(0, len(self.bottom_btns_degree)):
            self.bottom_btns_degree[i].grid(row=1, column=i)
        bottom_comparison_frame.grid(row=1, column=0)
        comparison_frame.grid(row=0, column=0, sticky=tk.NS)

        canvas_frame = ctk.CTkFrame(visualization_frame)
        self.top_canvas_label = ctk.CTkLabel(canvas_frame, text=f'{controller.top_structure.value}')
        self.canvas_top = ctk.CTkCanvas(canvas_frame, width=self.width, height=self.height, bg=white)
        self.bottom_canvas_label = ctk.CTkLabel(canvas_frame, text=f'{controller.bottom_structure.value}')
        self.canvas_bottom = ctk.CTkCanvas(canvas_frame, width=self.width, height=self.height, bg=white)
        self.top_canvas_label.pack(pady=(5, 0))
        self.canvas_top.pack()
        self.bottom_canvas_label.pack(pady=(5, 0))
        self.canvas_bottom.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        canvas_frame.grid(row=0, column=1)
        visualization_frame.pack(pady=(5, 0))

        self.buttons = [insert_button, delete_button, find_button, clear_button,
                        min_button, max_button, mean_button, median_button,
                        self.back_button, self.forward_button,
                        self.increase_size_button, self.decrease_size_button]
        self.buttons.extend(top_btns)
        self.buttons.extend(bottom_btns)
        self.buttons.extend(self.top_btns_degree)
        self.buttons.extend(self.bottom_btns_degree)
        controller.check_buttons()
        self.check_browsing_buttons(controller.history.pointer, len(controller.history.history_list))

        return frame

    def clear(self):
        self.canvas_top.delete('all')
        self.canvas_bottom.delete('all')

    def structure_change(self, controller, structure, mode):
        """
        Changes comparison structures in controller
        :param controller: controller to change the structure of
        :param structure: new structure key
        :param mode: determines whether to change top or bottom structure
        :return: returns nothing
        """
        tree_dict = {
            r.Structure.RBT: (rbt.RBTree, rbtv.RBTView),
            r.Structure.AVL: (avl.AVLTree, avlv.AVLView),
            r.Structure.BT: (bt.BTree, btv.BTView),
            r.Structure.BPT: (bpt.BPTree, bptv.BPTView),
            r.Structure.AVBT: (avbt.AVBTree, avbtv.AVBTView),
            r.Structure.AVBPT: (avbpt.AVBPTree, avbptv.AVBPTView),
            r.Structure.ASA: (asa.ASAGraph, asav.ASAGView)
        }
        if structure in tree_dict.keys():
            Tree = tree_dict[structure][0]
            View = tree_dict[structure][1]
            position = list(tree_dict.keys()).index(structure)
            if controller.top_structure != structure and mode == r.Mode.up:
                controller.clear()
                if position >= 2:
                    view = View(24, 18, 0, controller.top_tree_degree)
                    controller.top_tree = Tree(view, controller.top_tree_degree)
                    self.top_canvas_label.config(text=f'{structure.value} [degree: {controller.top_tree_degree}]')
                else:
                    view = View(26, 26, 0)
                    controller.top_tree = Tree(view)
                    self.top_canvas_label.config(text=f'{structure.value}')
                # Size change
                for i in range(self.size_value):
                    view.node_width += 6
                    view.node_height += 6
                    view.y_space += 12
                    view.y_above += 7
                controller.top_tree.update_positions(True)
                controller.top_tree.view.draw_tree(controller.top_tree.root, self.canvas_top, True)
                self.erase()
                # End size change
                # Speed change
                controller.top_tree.view.long_animation_time = controller.bottom_tree.view.long_animation_time
                controller.top_tree.view.short_animation_time = controller.bottom_tree.view.short_animation_time
                # End speed change
                view.create_GUI(controller, '')
                view.canvas_now = self.canvas_top
                controller.top_structure = structure
            elif controller.bottom_structure != structure and mode == r.Mode.down:
                controller.clear()
                if position >= 2:
                    view = View(24, 18, 0, controller.bottom_tree_degree)
                    controller.bottom_tree = Tree(view, controller.bottom_tree_degree)
                    self.bottom_canvas_label.config(text=f'{structure.value} [degree: {controller.bottom_tree_degree}]')
                else:
                    view = View(26, 26, 0)
                    controller.bottom_tree = Tree(view)
                    self.bottom_canvas_label.config(text=f'{structure.value}')
                # Size change
                for i in range(self.size_value):
                    view.node_width += 6
                    view.node_height += 6
                    view.y_space += 12
                    view.y_above += 7
                controller.bottom_tree.update_positions(True)
                controller.bottom_tree.view.draw_tree(controller.bottom_tree.root, self.canvas_bottom, True)
                self.erase()
                # End size change
                # Speed change
                controller.bottom_tree.view.long_animation_time = controller.top_tree.view.long_animation_time
                controller.bottom_tree.view.short_animation_time = controller.top_tree.view.short_animation_time
                # End speed change
                view.create_GUI(controller, '')
                view.canvas_now = self.canvas_bottom
                controller.bottom_structure = structure
            controller.check_buttons()
            self.set_browsing_buttons(False)

    def erase(self):
        self.canvas_top.delete('all')
        self.canvas_bottom.delete('all')
