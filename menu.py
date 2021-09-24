import tkinter as tk

def show_frame(frame):
    frame.tkraise()


root = tk.Tk()
root.state('zoomed')

root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)


f1 = tk.Frame(root)
f2 = tk.Frame(root)
f3 = tk.Frame(root)

for frame in (f1,f2,f3):
    frame.grid(row=0,column=0,sticky='nsew')

tk.Label(f1,text="Frame1",bg='red').pack(fill='x')
tk.Button(f1,text='Enter',command=lambda: show_frame(f2)).pack()

tk.Label(f2,text="Frame2",bg='green').pack(fill='x')
tk.Button(f2,text='Enter',command=lambda: show_frame(f3)).pack()

tk.Label(f3,text="Frame3",bg='yellow').pack(fill='x')
tk.Button(f3,text='Enter',command=lambda: show_frame(f1)).pack()

show_frame(f1)

root.mainloop()