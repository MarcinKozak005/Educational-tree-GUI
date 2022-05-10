import threading
import tkinter as tk


def wrap1():
    units = {
        'o11': (c1, 1, 2, 10),
        'o12': (c1, 3, 3, 20),
        'o13': (c1, 1, 0, 30)
    }
    animation_controller.add_movement(units, True)
    animation_controller.fst_finished = True
    animation_controller.move()
    animation_controller.fst_final_end = True


def wrap2():
    units = {
        'o21': (c2, 1, 2, 10),
        'o22': (c2, 3, 3, 20),
        'o23': (c2, 1, 0, 70)
    }
    animation_controller.add_movement(units, False)
    animation_controller.snd_finished = True
    animation_controller.move()
    # -----
    c2.create_text(70, 70, fill='black', text='Test string', tag='string1')
    for _ in range(100):
        root.after(10)
    c2.delete('string1')
    # -----
    animation_controller.add_movement(units, False)
    animation_controller.snd_finished = True
    animation_controller.move()
    animation_controller.snd_final_end = True


class AnimationController:
    def __init__(self):
        self.mode = 'double'
        self.fst_finished = False
        self.snd_finished = False
        self.lock = threading.Lock()
        self.fst_dict = {}
        self.snd_dict = {}
        self.fst_final_end = False
        self.snd_final_end = False

    def add_movement(self, object_dict, first):
        for k in object_dict.keys():
            if first:
                self.fst_dict[k] = object_dict[k]
            else:
                self.snd_dict[k] = object_dict[k]

    def reset(self):
        self.fst_finished = False
        self.snd_finished = False
        self.fst_dict = {}
        self.snd_dict = {}
        self.fst_final_end = False
        self.snd_final_end = False

    def move(self):
        if self.mode == 'double':
            while not (self.fst_finished or self.fst_final_end) and (self.snd_finished or self.snd_final_end):
                print(f'{threading.current_thread().name}')
            with self.lock:
                if (self.fst_finished or self.fst_final_end) and (self.snd_finished or self.snd_final_end):
                    while self.fst_dict or self.snd_dict:
                        if self.fst_dict:
                            tmp = {}
                            for k in self.fst_dict:
                                data = self.fst_dict[k]
                                data[0].move(k, data[1], data[2])
                                if data[3] > 0:
                                    self.fst_dict[k] = (data[0], data[1], data[2], data[3] - 1)
                                    tmp[k] = self.fst_dict[k]
                            self.fst_dict = tmp
                        if self.snd_dict:
                            tmp = {}
                            for k in self.snd_dict:
                                data = self.snd_dict[k]
                                data[0].move(k, data[1], data[2])
                                if data[3] > 0:
                                    self.snd_dict[k] = (data[0], data[1], data[2], data[3] - 1)
                                    tmp[k] = self.snd_dict[k]
                            self.snd_dict = tmp
                        root.after(10)
                        root.update()
                    self.fst_finished, self.snd_finished = False, False
                    self.fst_final_end, self.snd_final_end = False, False
        elif self.mode == 'single':  # może da się połączyć z tym wyżej ???
            while self.fst_dict:
                tmp = {}
                for k in self.fst_dict:
                    data = self.fst_dict[k]
                    data[0].move(k, data[1], data[2])
                    if data[3] > 0:
                        self.fst_dict[k] = (data[0], data[1], data[2], data[3] - 1)
                        tmp[k] = self.fst_dict[k]
                root.after(10)
                root.update()
                self.fst_dict = tmp
            self.fst_finished = False
            self.fst_final_end = False
            self.fst_dict = {}


def execute1():
    animation_controller.reset()
    animation_controller.mode = 'single'
    wrap1()


def execute2():
    animation_controller.reset()
    animation_controller.mode = 'double'
    threading.Thread(target=wrap2).start()
    wrap1()


# ---


root = tk.Tk()

c1 = tk.Canvas(root, bg='#FFFFFF', width=500, height=300)
c2 = tk.Canvas(root, bg='#FFFFFF', width=500, height=300)

tk.Button(root, text='Single', command=execute1).pack()
tk.Button(root, text='Double', command=execute2).pack()

c1.pack()
c1.create_oval(30, 30, 50, 50, fill='red', tags='o11')
c1.create_oval(50, 50, 70, 70, fill='pink', tags='o12')
c1.create_oval(80, 80, 100, 100, fill='yellow', tags='o13')
c2.pack()
c2.create_oval(30, 30, 50, 50, fill='blue', tags='o21')
c2.create_oval(30, 50, 50, 70, fill='green', tags='o22')
c2.create_oval(50, 30, 70, 50, fill='purple', tags='o23')
animation_controller = AnimationController()

root.mainloop()
