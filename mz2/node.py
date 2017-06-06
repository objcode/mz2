class Node(object):
    left = None
    right = None
    top = None
    bottom = None

    links = None

    hi = None
    on_path = False

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.links = []

    def mark_on_path(self):
        self.on_path = True

    def path_neighbors(self):
        if not self.on_path:
            return []

        return [a for a in self.links if a.on_path]

    def is_deadend(self):
        return len(self.links) == 1

    def is_unconnected(self):
        return not self.links

    def adjacent(self):
        return [n for n in [self.left, self.right, self.top, self.bottom] if n]

    def unlinked(self):
        return list(set(self.adjacent()).difference(self.links))

    def hilite(self, char):
        self.hi = char

    def link(self, other, bidi=True):
        self.links.append(other)
        if bidi:
            other.links.append(self)

    def is_linked(self, other):
        return other is not None and other in self.links

    def __str__(self):
        items = ["", "", "", ""]
        if self.is_linked(self.left):
            items[0] = "<"
        if self.is_linked(self.right):
            items[1] = ">"
        if self.is_linked(self.top):
            items[2] = "^"
        if self.is_linked(self.bottom):
            items[3] = "B"

        return "(%s, %s)[%s]" % (self.row, self.col, ', '.join([item for item in items if item.strip()]));

    def clean_str(self):
        items = [" ", " ", " ", " "];
        if not self.left or not self.is_linked(self.left):
            items[0] = "|"
        if not self.right or not self.is_linked(self.right):
            items[1] = "|"
        if not self.top or not self.is_linked(self.top):
            items[2] = "="
        if not self.bottom or not self.is_linked(self.bottom):
            items[3] = "="

        if items[2] == '=' and items[0] == ' ':
            first_row = '=='
        elif items[2] == ' ' and items[0] == '|':
            first_row = '| '
        else:
            first_row = ''.join(['=', items[2]])
        if not self.top:
            first_row = "=="

        extra_row = ""
        if not self.bottom:
            extra_row = "=="

        me = " " if self.links else "?"
        me = "*" if self.on_path else me

        last_char = ""
        if not self.right:
            last_char = '|'
            first_row += "=" if not self.top else "|"
            extra_row += "=" if not self.bottom else ""

        middle_row = ''.join([items[0], self.hi if self.hi else me, last_char])

        return '\n'.join([first_row, middle_row, extra_row])
