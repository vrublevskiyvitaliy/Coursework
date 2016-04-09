from tkinter import *


def close_window(ev):
    global root
    root.destroy()

root = Tk()


def init():
    panel_frame = Frame(root, height=60, bg='gray')
    view_frame = Frame(root, height=340, width=600)

    panel_frame.pack(side='top', fill='x')
    view_frame.pack(side='bottom', fill='both', expand=1)

    quit_btn = Button(panel_frame, text='Quit')

    quit_btn.bind("<Button-1>", close_window)

    quit_btn.place(x=10, y=10, width=40, height=40)

    root.mainloop()