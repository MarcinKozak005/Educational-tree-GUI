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
        comparison_frame = ctk.CTkFrame(visualization_frame)
        top_comparison_frame = tk.Frame(comparison_frame, height=self.height + 35)
        top_comparison_frame.grid_propagate(0)
        bottom_comparison_frame = tk.Frame(comparison_frame)

        # Short versions
        bcf = bottom_comparison_frame
        tcf = top_comparison_frame
        c = controller
        st = r.Structure
        up = r.Mode.up
        down = r.Mode.down
        cba = comparison_buttons_argument

        b1t = ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.RBT, up), text='Red-black', **cba)
        b2t = ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.AVL, up), text='AVL', **cba)
        b3t = ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.BT, up), text='B-', **cba)
        b4t = ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.BPT, up), text='B+', **cba)
        b5t = ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.AVBT, up), text='AVB-', **cba)
        b6t = ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.AVBPT, up), text='AVB+', **cba)
        b7t = ctk.CTkButton(tcf, command=lambda: self.structure_change(c, st.ASA, up), text='ASA', **cba)
        degree_btn_frame1 = tk.Frame(tcf)
        db3t = ctk.CTkButton(degree_btn_frame1, text='3', **btn_arg)
        db4t = ctk.CTkButton(degree_btn_frame1, text='4', **btn_arg)
        db5t = ctk.CTkButton(degree_btn_frame1, text='5', **btn_arg)
        db6t = ctk.CTkButton(degree_btn_frame1, text='6', **btn_arg)

        b1b = ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.RBT, down), text='Red-black', **cba)
        b2b = ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.AVL, down), text='AVL', **cba)
        b3b = ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.BT, down), text='B-', **cba)
        b4b = ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.BPT, down), text='B+', **cba)
        b5b = ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.AVBT, down), text='AVB-', **cba)
        b6b = ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.AVBPT, down), text='AVB+', **cba)
        b7b = ctk.CTkButton(bcf, command=lambda: self.structure_change(c, st.ASA, down), text='ASA', **cba)
        degree_btn_frame2 = tk.Frame(bcf)
        db3b = ctk.CTkButton(degree_btn_frame2, text='3', **btn_arg)
        db4b = ctk.CTkButton(degree_btn_frame2, text='4', **btn_arg)
        db5b = ctk.CTkButton(degree_btn_frame2, text='5', **btn_arg)
        db6b = ctk.CTkButton(degree_btn_frame2, text='6', **btn_arg)

        ctk.CTkLabel(top_comparison_frame, text='Top structure').grid(row=0, column=0)
        b1t.grid(row=1, column=0, pady=(0, 2))
        b2t.grid(row=2, column=0, pady=(0, 2))
        b3t.grid(row=3, column=0, pady=(0, 2))
        b4t.grid(row=4, column=0, pady=(0, 2))
        b5t.grid(row=5, column=0, pady=(0, 2))
        b6t.grid(row=6, column=0, pady=(0, 2))
        b7t.grid(row=7, column=0, pady=(0, 2))
        degree_btn_frame1.grid(row=8, column=0)
        ctk.CTkLabel(degree_btn_frame1, text='Max graph degree:').grid(row=0, column=0, columnspan=4)
        db3t.grid(row=1, column=0)
        db4t.grid(row=1, column=1)
        db5t.grid(row=1, column=2)
        db6t.grid(row=1, column=3)
        top_comparison_frame.grid(row=0, column=0, sticky=tk.NSEW)

        ctk.CTkLabel(bottom_comparison_frame, text='Bottom structure').grid(row=0, column=1)
        b1b.grid(row=1, column=1, pady=(0, 2))
        b2b.grid(row=2, column=1, pady=(0, 2))
        b3b.grid(row=3, column=1, pady=(0, 2))
        b4b.grid(row=4, column=1, pady=(0, 2))
        b5b.grid(row=5, column=1, pady=(0, 2))
        b6b.grid(row=6, column=1, pady=(0, 2))
        b7b.grid(row=7, column=1, pady=(0, 2))
        degree_btn_frame2.grid(row=8, column=1)
        ctk.CTkLabel(degree_btn_frame2, text='Max graph degree:').grid(row=0, column=0, columnspan=4)
        db3b.grid(row=1, column=0)
        db4b.grid(row=1, column=1)
        db5b.grid(row=1, column=2)
        db6b.grid(row=1, column=3)
        bottom_comparison_frame.grid(row=1, column=0)
        comparison_frame.grid(row=0, column=0, sticky=tk.NS)

        canvas_frame = ctk.CTkFrame(visualization_frame)
        self.top_canvas_label = ctk.CTkLabel(canvas_frame, text=f'TOP')
        self.canvas_top = ctk.CTkCanvas(canvas_frame, width=self.width, height=self.height, bg=white)
        self.bottom_canvas_label = ctk.CTkLabel(canvas_frame, text=f'BOTTOM')
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
            controller.clear()
            Tree = tree_dict[structure][0]
            View = tree_dict[structure][1]
            position = list(tree_dict.keys()).index(structure)
            if mode == r.Mode.up:
                if position >= 2:
                    view = View(24, 18, 0, controller.top_tree_degree)
                    controller.top_tree = Tree(view, controller.top_tree_degree)
                else:
                    view = View(26, 26, 0)
                    controller.top_tree = Tree(view)
                view.create_GUI(controller, '')
                view.canvas_now = self.canvas_top
                controller.top_structure = structure
            elif mode == r.Mode.down:
                if position >= 2:
                    view = View(24, 18, 0, controller.bottom_tree_degree)
                    controller.bottom_tree = Tree(view, controller.bottom_tree_degree)
                else:
                    view = View(26, 26, 0)
                    controller.bottom_tree = Tree(view)
                view.create_GUI(controller, '')
                view.canvas_now = self.canvas_bottom
                controller.bottom_structure = structure
