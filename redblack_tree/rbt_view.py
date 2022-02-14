import tkinter as tk
import core.menu as m

import core.root as r
import redblack_tree.rbt_model as rbt


class View:
    def __init__(self, width, height, y_space, y_above, node_size, animation_time, animation_unit, layout):
        self.explanation = Explanation()
        self.width = width
        self.height = height
        self.y_space = y_space
        self.y_above = y_above
        self.node_size = node_size
        self.half_node_size = node_size / 2
        self.animation_time = animation_time
        self.animation_unit = animation_unit
        self.layout = layout
        self.canvas_now = None
        self.canvas_prev = None
        self.info_label = None
        self.explanation_label = None
        self.buttons = []
        self.prev_label = None
        self.frame31 = None
        self.now_label = None
        self.view_button = None

    def create_GUI(self, controller, model):

        frame = tk.Frame(r.frame)

        frame1 = tk.LabelFrame(frame, text='1')
        tk.Label(frame1, text='RedBlack Tree', bg='red', height=2).pack(fill='x')  # do poprawy +-
        frame1.pack(fill='x')

        frame2 = tk.LabelFrame(frame, text='2')
        insert_field = tk.Entry(frame2)
        insert_button = tk.Button(frame2, text='Add node',
                                  command=lambda: controller.perform(model, 'insert', insert_field.get()))
        delete_field = tk.Entry(frame2)
        delete_button = tk.Button(frame2, text='Delete node',
                                  command=lambda: controller.perform(model, 'delete', delete_field.get()))
        find_field = tk.Entry(frame2)
        find_button = tk.Button(frame2, text='Find node',
                                command=lambda: controller.perform(model, 'search', find_field.get()))
        clear_button = tk.Button(frame2, text='Clear tree', command=lambda: controller.clear())
        self.view_button = tk.Button(frame2, text='Show previous state and explanation: ON',
                                     command=lambda: controller.change_layout())
        back_button = tk.Button(frame2, text='Back to menu', command=lambda: r.show_frame(m.frame))
        self.info_label = tk.Label(frame2)
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
        frame2.pack()

        frame3 = tk.LabelFrame(frame, text='3')
        self.frame31 = tk.Frame(frame3)
        explanation_title_lab = tk.Label(self.frame31)
        self.explanation_label = tk.Label(self.frame31)
        self.explanation_label.config(text='', justify=tk.LEFT, width=70, anchor=tk.W)
        explanation_title_lab.config(text='Explanation', font=15)
        explanation_title_lab.pack()
        self.explanation_label.pack()
        self.frame31.grid(row=0, column=0, sticky='NS')

        frame32 = tk.Frame(frame3)
        self.prev_label = tk.Label(frame32, text='Previous state of the tree:')
        self.canvas_prev = tk.Canvas(frame32, width=self.width, height=self.height, bg='white')
        self.now_label = tk.Label(frame32, text='Current state of the tree:')
        self.canvas_now = tk.Canvas(frame32, width=self.width, height=self.height, bg='white')
        self.prev_label.pack(pady=(5, 0))
        self.canvas_prev.pack()
        self.now_label.pack(pady=(5, 0))
        self.canvas_now.pack()
        frame32.grid(row=0, column=1)
        #
        def tests():
            cases = [
                [1,2,3],
                [3,2,1],
                [2,1,3,4,5],
                [2,1,5,4,3],
                [1,3,2],
                [3,1,2],
                [4,5,3,2,1],
                [4,5,1,2,3]
            ]
            for case in cases:
                for c in case:
                    controller.perform(model, 'insert', str(c))
                _ = input("Press sth to process")
                model.clear()
        tk.Button(frame, text='Tests', command=tests).pack()
        #
        frame3.pack()

        self.buttons = [insert_button, delete_button, find_button, clear_button, self.view_button]

        return frame

    def draw_exp_text(self, node, exp_str, above=True):
        txt = self.canvas_now.create_text(node.x, node.y + (-1 if above else 1) * self.node_size, fill='white',
                                          text=exp_str,
                                          tags='exp_txt')
        txt_bg = self.canvas_now.create_rectangle(self.canvas_now.bbox(txt), fill="grey", tags='exp_txt')
        self.canvas_now.tag_lower(txt_bg)
        r.frame.update()
        r.frame.after(self.animation_time)  # funkcja wait?
        self.canvas_now.delete('exp_txt')
        self.explanation.append(exp_str)

    def draw_subtree(self, node, canvas):
        if type(node) is not rbt.RBTree.RBLeaf:
            if type(node.right) is not rbt.RBTree.RBLeaf:
                self.draw_line(canvas, node, node.right, tags=[f'Line{node.__hash__()}', 'Line'])
            if type(node.left) is not rbt.RBTree.RBLeaf:
                self.draw_line(canvas, node, node.left, tags=[f'Line{node.__hash__()}', 'Line'])
            canvas.create_oval(node.x - self.half_node_size, node.y - self.half_node_size, node.x + self.half_node_size,
                               node.y + self.half_node_size, fill=node.color, tags=f'Node{node.__hash__()}')
            canvas.create_text(node.x, node.y, fill='white', text=node.value, tags=f'Node{node.__hash__()}')

    def draw_line(self, canvas, node1, node2, tags=None):
        if node1 is not None and node2 is not None and type(node1) is not rbt.RBTree.RBLeaf and type(
                node2) is not rbt.RBTree.RBLeaf:
            canvas.create_line(node1.x, node1.y, node2.x, node2.y, fill='black', tags=tags)

    def set_buttons(self, value):
        for b in self.buttons:  # dodawane z jakiegoś add buton do view?
            b.config(state='normal' if value else 'disabled')

    def draw_recolor_text(self, node, to_color):
        if type(node) is rbt.RBTree.RBNode:
            txt = self.canvas_now.create_text(node.x, node.y - self.node_size, fill='white',
                                              text=f'Change color to {to_color}',
                                              tags='recolor_txt')
            txt_bg = self.canvas_now.create_rectangle(self.canvas_now.bbox(txt), fill="grey", tags='recolor_txt')
            self.explanation.append(f'Change color of {node.value} to {to_color}')
            self.canvas_now.tag_lower(txt_bg)

    # Bardziej RBTree niż inne drzewa
    def animate_rotations(self, node):
        successors = node.successors()
        units = {}
        tmp = self.animation_time / self.animation_unit
        for s in successors:
            x_unit = (s.x_next - s.x) / tmp
            y_unit = (s.y_next - s.y) / tmp
            units[s] = (x_unit, y_unit)
        while tmp > 0:
            for s in successors:
                self.rotation_tick(s, units[s][0], units[s][1])
            r.frame.after(self.animation_unit)
            r.frame.update()
            tmp -= 1

    def rotation_tick(self, node, x_unit, y_unit):
        self.canvas_now.delete(f'Line{node.__hash__()}')
        self.canvas_now.delete(f'Line{node.parent.__hash__()}')
        self.canvas_now.move(f'Node{node.__hash__()}', x_unit, y_unit)
        node.x += x_unit
        node.y += y_unit
        self.draw_line(self.canvas_now, node, node.right, tags=[f'Line{node.__hash__()}', 'Line'])
        self.draw_line(self.canvas_now, node, node.left, tags=[f'Line{node.__hash__()}', 'Line'])
        if node.parent is not None:
            self.draw_line(self.canvas_now, node.parent, node.parent.right,
                           tags=[f'Line{node.parent.__hash__()}', 'Line'])
            self.draw_line(self.canvas_now, node.parent, node.parent.left,
                           tags=[f'Line{node.parent.__hash__()}', 'Line'])
        self.canvas_now.tag_lower('Line')

    # Canvas visualization
    def draw_rb_tree(self, tree, canvas):
        if type(tree) is not rbt.RBTree.RBLeaf and tree is not None:
            self.draw_subtree(tree, canvas)
            self.draw_rb_tree(tree.left, canvas)
            self.draw_rb_tree(tree.right, canvas)

    def draw_node(self, node, canvas):
        if type(node) is rbt.RBTree.RBNode:
            canvas.create_oval(node.x - self.half_node_size, node.y - self.half_node_size, node.x + self.half_node_size,
                               node.y + self.half_node_size, fill=node.color, tags=f'Node{node.__hash__()}')
            canvas.create_text(node.x, node.y, fill='white', text=node.value, tags=f'Node{node.__hash__()}')

    def move_object(self, obj, x1, y1, x2, y2):
        x_diff = x2 - x1
        y_diff = y2 - y1
        x_unit = x_diff / (self.animation_time / self.animation_unit)
        y_unit = y_diff / (self.animation_time / self.animation_unit)
        counter = self.animation_time / self.animation_unit
        while counter > 0:
            self.canvas_now.move(obj, x_unit, y_unit)
            r.frame.update()
            self.canvas_now.after(self.animation_unit)
            counter -= 1

    def clear(self):
        self.canvas_prev.delete('all')
        self.canvas_now.delete('all')
        self.explanation_label.config(text='')

    def prepare_view(self):
        self.info_label.config(text='')
        self.canvas_now.delete('all')
        self.explanation_label.config(text=self.explanation.string, wraplength=400)
        self.explanation.reset()


class Explanation:
    string = ''
    line = 1

    def __init__(self):
        pass

    def append(self, text):
        self.string += f'[{self.line}] {text}\n'
        self.line += 1

    def reset(self):
        self.string = ''
        self.line = 1
