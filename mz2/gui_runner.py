import time
from Tkinter import *

class GuiRunner(object):

    def __init__(self, fn, draw_path=False, flood_center=False):
        self.fn = fn
        self.draw_path = draw_path
        self.flood_center = flood_center
        self.last_drawn = None

    def __call__(self, grid, **kwargs):
        self.grid = grid
        gen = self.fn(grid, **kwargs)
        grid.callback = self.draw
        self.make_window()
        self.draw_grid()
        self.flush()
        for trial in gen:
            self.draw(trial, cursor=trial)
            self.flush()
            time.sleep(0.2)
        self.draw_grid()
        self.tk.mainloop()

    def draw(self, cell, cursor=None, refresh_last=True):
        if refresh_last and self.last_drawn:
            self.draw(self.last_drawn, cursor=cursor, refresh_last=False)
        self.last_drawn = cell
        cell_width = int(1.0 * (self.width - 6) / self.grid.width)
        cell_height = int(1.0 * (self.height - 6) / self.grid.height)
        top = 3 + cell.row * cell_height
        left = 3 + cell.col * cell_width
        if cell == cursor:
            fill = "orange"
        else:
            fill = "white"
        self.canvas.create_rectangle(left, top, left + cell_width, top + cell_height, fill=fill, outline=fill)
        if not cell.is_linked(cell.top):
            color = "black"
        else:
            color = "white"
        self.canvas.create_line(left, top, left + cell_width, top, fill=color)
        if not cell.is_linked(cell.bottom):
            color = "black"
        else:
            color = "white"
        self.canvas.create_line(left, top + cell_height, left + cell_width, top + cell_height, fill=color)
        if not cell.is_linked(cell.left):
            color = "black"
        else:
            color = "white"
        self.canvas.create_line(left, top, left, top + cell_height, fill=color)
        if not cell.is_linked(cell.right):
            color = "black"
        else:
            color = "white"
        self.canvas.create_line(left + cell_width, top, left + cell_width, top + cell_height, fill=color)


    def flush(self):
        self.tk.update_idletasks()
        self.tk.update()

    def draw_grid(self):
        for row in self.grid.iterrows():
            for cell in row:
                self.draw(cell)

    def make_window(self):
        self.tk = Tk()
        ratio = 1.0 * self.grid.width / self.grid.height
        self.width = int(800 * ratio) if ratio < 1 else 800
        self.height = 800 if ratio < 1 else 800 / ratio
        self.canvas = Canvas(master=self.tk, width=self.width, height=self.height)
        self.canvas.pack()
