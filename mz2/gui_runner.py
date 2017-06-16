import time
from Tkinter import *

from colour import Color

DARK="#1E2227"
GRAY="#414954"
LIGHT="#F9FCFC"

COLOR="#C2E2E8"
ACCENT="#EA6912"

class GuiRunner(object):

    def __init__(self, delay=0, center_flood=False, mark_path=False, skulls=False):
        self.delay = delay
        self.draw_path = mark_path
        self.flood_center = center_flood
        self.skulls = skulls

        self.cursor = None
        self.draws = {}
        self.first_link = None
        self.max_distance = 1

    def __call__(self, fn):
        return self.render_loop(fn)

    def render_loop(self, fn):
        def loop(grid, **kwargs):
            self.grid = grid
            self.max_distance = int(0.5 * self.grid.width * self.grid.height)
            gen = fn(grid, **kwargs)
            grid.callback = self.onlink
            self.make_window()
            self.set_title(fn)
            self.draw_grid()
            self.flush()
            for trial in gen:
                self.update_cursor(trial)
                self.flush()
                if self.delay:
                    time.sleep(self.delay * 0.01)

            if self.draw_path:
                grid.draw_longest_path()
            if self.flood_center:
                self.do_flood()
            self.update_cursor(None)
            self.draw_grid()
            self.tk.mainloop()
        return loop

    def onlink(self, first, second):
        if first:
            self.draw(first)
        if second:
            self.draw(second)
        if second is not None and self.flood_center:
            if self.first_link is None:
                self.first_link = second
            self.do_flood()

    def update_cursor(self, cursor):
        old_cursor = self.cursor
        self.cursor = cursor;
        if old_cursor:
            self.draw(old_cursor)
        if self.cursor:
            self.draw(self.cursor)

    def do_flood(self):
        old_distances = self.grid.distances
        self.grid.flood_center(self.first_link)
        new_distances = self.grid.distances
        cells = set(new_distances.cells())
        if old_distances:
            cells = cells.union(old_distances.cells())
        for cell in cells:
            old = old_distances[cell] if old_distances else None
            new = new_distances[cell]
            if old != new:
                self.draw(cell)

    def draw(self, cell):
        cell_width = int(1.0 * (self.width - 6) / self.grid.width)
        cell_height = int(1.0 * (self.height - 6) / self.grid.height)
        top = 3 + cell.row * cell_height
        left = 3 + cell.col * cell_width

        if cell in self.draws:
            old_draws = self.draws[cell]
            [self.canvas.delete(item) for item in old_draws]
        this_draw = []
        self.draws[cell] = this_draw


        # first do any distance backgrounds
        if self.grid.distances and cell in self.grid.distances.cells():
            distance = self.grid.distances[cell]
            ratio = 1.0 * distance / self.max_distance if self.max_distance else 0
            color = Color(COLOR)
            color.hue = ratio
            tag = self.canvas.create_rectangle(
                left,
                top,
                left + cell_width,
                top + cell_height,
                fill=color.hex,
                outline=''
            )
            this_draw.append(tag)

        if cell == self.cursor:
            fill = ACCENT
            tag = self.canvas.create_oval(left + cell_width / 4, top + cell_height / 4, left + 3 * cell_width / 4, top + 3 * cell_height / 4, fill=fill, outline=fill)
            this_draw.append(tag)
        elif self.skulls and cell.is_deadend() and not cell.on_path:
            # never draw deadends at cursor or on a path
            tag = self.canvas.create_text(left + cell_width / 2, top + cell_height / 2, text=u"\u2620", fill="red")
            this_draw.append(tag)

        if cell.on_path:
            neighbors = cell.path_neighbors()
            center = (left + cell_width / 2, top + cell_height / 2)
            if cell.top in neighbors or cell.bottom in neighbors:
                top_offset = -1 *  cell_height / 2 if cell.top in neighbors else 0
                bottom_offset = cell_height / 2 if cell.bottom in neighbors else 0
                tag = self.canvas.create_line(center[0],
                                              center[1] + top_offset,
                                              center[0],
                                              center[1] + bottom_offset,
                                              fill=GRAY)
                this_draw.append(tag)

            if cell.left in neighbors or cell.right in neighbors:
                left_offset = -1 *  cell_width / 2 if cell.left in neighbors else 0
                right_offset = cell_width / 2 if cell.right in neighbors else 0
                tag = self.canvas.create_line(center[0] + left_offset,
                                              center[1],
                                              center[0] + right_offset,
                                              center[1],
                                              fill=GRAY)
                this_draw.append(tag)

            if cell.is_deadend():
                size = max(2, cell_width / 2)
                center = (left + cell_width / 2, top + cell_height / 2)
                tag = self.canvas.create_oval(
                    center[0] - size / 2,
                    center[1] - size / 2,
                    center[0] + size / 2,
                    center[1] + size / 2,
                    fill=ACCENT,
                    outline=ACCENT)
                this_draw.append(tag)

        color = LIGHT if cell.is_unconnected() else DARK

        if not cell.is_linked(cell.top):
            tag = self.canvas.create_line(left, top, left + cell_width, top, fill=color)
            this_draw.append(tag)

        if not cell.is_linked(cell.left):
            tag = self.canvas.create_line(left, top, left, top + cell_height, fill=color)
            this_draw.append(tag)

        if not cell.is_linked(cell.bottom):
            tag = self.canvas.create_line(left, top + cell_height, left + cell_width, top + cell_height, fill=color)
            this_draw.append(tag)

        if not cell.is_linked(cell.right):
            tag = self.canvas.create_line(left + cell_width, top, left + cell_width, top + cell_height, fill=color)
            this_draw.append(tag)


    def flush(self):
        self.tk.update_idletasks()
        self.tk.update()

    def draw_grid(self, cursor=None):
        self.canvas.delete("all")
        self.draws = {}
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

    def set_title(self, fn):
        args = []
        args.append("height: %s, width: %s" % (self.grid.height, self.grid.width))
        args.append("wait: %s " % (self.delay,) if self.delay else None)
        args.append("flood_center" if self.flood_center else None)
        args.append("draw_path" if self.draw_path else None)
        args = [a for a in args if a]
        dword = "(%s)" % (", ".join(args)) if args else ""
        self.tk.title("%s => %s %s" % (fn.__module__.split('.')[-1], fn.__name__, dword))
