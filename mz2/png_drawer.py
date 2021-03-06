import os

CELL_WIDTH = 30
CELL_HEIGHT = 20
BORDER_THICKNESS = 3
EDGE_PADDING = 50

class PngDrawer(object):

    def __init__(self, file_path, grid,
                 cell_width=CELL_WIDTH,
                 cell_height=CELL_HEIGHT,
                 border_thickness=BORDER_THICKNESS,
                 edge_padding=EDGE_PADDING,
                 color="#aa5000",
                 path="#3350aa"):
      self.file_path = file_path
      self.grid = grid
      self.cell_dim = (cell_width, cell_height)
      self.border_thickness = border_thickness
      self.edge_padding = edge_padding
      self.color = color
      self.path_color = path


    def im_size(self):
        return (
            self.edge_padding + self.grid.width * self.cell_dim[0] + self.border_thickness * 2,
            self.edge_padding + self.grid.height * self.cell_dim[1] + self.border_thickness * 2)

    def draw(self):
        from PIL import Image, ImageDraw
        im = Image.new("RGB", self.im_size(), "white")
        pen = ImageDraw.Draw(im)

        distances = self.grid.distances
        if distances:
            _, max_distance = distances.max()

        for y, row, in enumerate(self.grid.iterrows()):
            for x, cell in enumerate(row):
                left = (self.edge_padding / 2) + self.cell_dim[0] * x
                top = (self.edge_padding / 2) + self.cell_dim[1] * y

                if distances and max_distance:
                    current = distances[cell]
                    if current is None:
                        fill = (0x33, 0x33, 0x33)
                    else:
                        pct = .3 * current / max_distance
                        fill = (int(0xEE * pct), 0x11, int(0x100 * pct))
                    points = [(left, top),
                              (left + self.cell_dim[0], top + self.cell_dim[1])]
                    pen.rectangle(points, fill = fill)

                if not cell.is_linked(cell.left):
                    pen.line([(left, top),
                              (left, top + self.cell_dim[1])],
                             fill=self.color,
                             width=self.border_thickness)
                if not cell.is_linked(cell.top):
                    pen.line([(left, top),
                              (left + self.cell_dim[0], top)],
                             fill=self.color,
                             width=self.border_thickness)
                if not cell.right:
                    pen.line([(left + self.cell_dim[0], top),
                              (left + self.cell_dim[0], top + self.cell_dim[1])],
                             fill=self.color,
                             width=self.border_thickness)
                if not cell.bottom:
                    btop = top + self.cell_dim[1]
                    pen.line([(left, btop),
                              (left + self.cell_dim[0], btop)],
                             fill=self.color,
                             width=self.border_thickness)

                for path in cell.path_neighbors():
                    center = (left + self.cell_dim[0] / 2, top + self.cell_dim[1] / 2)

                    if path == cell.top:
                        pen.line([center,
                                  (center[0], center[1] - self.cell_dim[1])],
                                 fill=self.path_color,
                                 width=self.border_thickness)
                    elif path == cell.bottom:
                        pen.line([center,
                                  (center[0], center[1] + self.cell_dim[1])],
                                 fill=self.path_color,
                                 width=self.border_thickness)
                    elif path == cell.right:
                        pen.line([center,
                                  (center[0] + self.cell_dim[0], center[1])],
                                 fill=self.path_color,
                                 width=self.border_thickness)
                    elif path == cell.left:
                        pen.line([center,
                                  (center[0] - self.cell_dim[0], center[1])],
                                 fill=self.path_color,
                                 width=self.border_thickness)

        del pen
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
        im.save(self.file_path, "PNG")
