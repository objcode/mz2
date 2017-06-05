
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
                 color="#aa5000"):
      self.file_path = file_path
      self.grid = grid
      self.cell_dim = (cell_width, cell_height)
      self.border_thickness = border_thickness
      self.edge_padding = edge_padding
      self.color = color


    def im_size(self):
        return (
            self.edge_padding + self.grid.width * self.cell_dim[0] + self.border_thickness * 2,
            self.edge_padding + self.grid.height * self.cell_dim[1] + self.border_thickness * 2)

    def draw(self):
        from PIL import Image, ImageDraw
        im = Image.new("RGB", self.im_size(), "white")
        pen = ImageDraw.Draw(im)

        for y, row, in enumerate(self.grid.iterrows()):
            for x, cell in enumerate(row):
                left = (self.edge_padding / 2) + self.cell_dim[0] * x
                top = (self.edge_padding / 2) + self.cell_dim[1] * y

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

        del pen
        im.save(self.file_path, "PNG")
