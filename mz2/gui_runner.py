

class GuiRunner(object):

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, grid, **kwargs):
        gen = self.fn(grid, **kwargs)
        for trial in gen:
            pass
        print grid
