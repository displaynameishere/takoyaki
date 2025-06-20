import curses
import re

class TakoApp:
    def __init__(self, stdscr, min_rows=24, min_cols=80, bg_color="#000000", fg_color="#FFFFFF", title=""):
        self.stdscr = stdscr
        self.min_rows = min_rows
        self.min_cols = min_cols
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.title = title
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)
        self.check_size()
        self.init_colors()
        self.stdscr.bkgd(' ', curses.color_pair(1))
        self.stdscr.clear()

    def check_size(self):
        rows, cols = self.stdscr.getmaxyx()
        if rows < self.min_rows or cols < self.min_cols:
            curses.endwin()
            raise RuntimeError(f"[takoui] Terminal too small: {cols}x{rows} min: {self.min_cols}x{self.min_rows}")

    def init_colors(self):
        self.color_map = {}
        self.color_pairs = {}
        curses.init_pair(1, self.rgb_to_curses(self.fg_color), self.rgb_to_curses(self.bg_color))
        self.color_pairs[(self.fg_color, self.bg_color)] = 1

    def rgb_to_curses(self, hexcolor):
        r, g, b = self.hex_to_rgb(hexcolor)
        return self.rgb_to_256color(r, g, b)

    def hex_to_rgb(self, h):
        h = h.lstrip('#')
        lv = len(h)
        return tuple(int(h[i:i+lv//3], 16) for i in range(0, lv, lv//3))

    def rgb_to_256color(self, r, g, b):
        r = int(r / 255 * 5)
        g = int(g / 255 * 5)
        b = int(b / 255 * 5)
        return 16 + 36 * r + 6 * g + b

    def get_color_pair(self, fg, bg):
        if (fg, bg) in self.color_pairs:
            return curses.color_pair(self.color_pairs[(fg, bg)])
        n = len(self.color_pairs) + 1
        if n > curses.COLOR_PAIRS - 1:
            return curses.color_pair(1)
        curses.init_pair(n, self.rgb_to_curses(fg), self.rgb_to_curses(bg))
        self.color_pairs[(fg, bg)] = n
        return curses.color_pair(n)

    def draw_title(self):
        self.stdscr.attrset(self.get_color_pair(self.fg_color, self.bg_color) | curses.A_BOLD)
        self.stdscr.addstr(0, 0, ' ' * (self.min_cols))
        t = self.title[:self.min_cols]
        self.stdscr.addstr(0, 0, t)
        self.stdscr.attrset(self.get_color_pair(self.fg_color, self.bg_color))

    def menu(self, y, x, options):
        idx = 0
        n = len(options)
        while True:
            for i, opt in enumerate(options):
                attr = curses.A_REVERSE if i == idx else curses.A_NORMAL
                self.stdscr.attrset(self.get_color_pair(self.fg_color, self.bg_color) | attr)
                self.stdscr.addstr(y + i, x, ' ' * (self.min_cols - x))
                self.stdscr.addstr(y + i, x, opt[:self.min_cols - x - 1])
            self.stdscr.refresh()
            k = self.stdscr.getch()
            if k in (curses.KEY_UP, ord('k')):
                idx = (idx - 1) % n
            elif k in (curses.KEY_DOWN, ord('j')):
                idx = (idx + 1) % n
            elif k in (curses.KEY_ENTER, 10, 13):
                return idx
            elif k == 27:
                return -1

    def preview_text(self, y, x, text, width, height):
        lines = self.wrap_text(text, width)
        pattern = re.compile(r'<#([0-9a-fA-F]{6})>')
        for i in range(min(height, len(lines))):
            line = lines[i]
            self.stdscr.move(y + i, x)
            pos = 0
            col = x
            fg = self.fg_color
            while pos < len(line):
                m = pattern.search(line, pos)
                if m and m.start() == pos:
                    fg = "#" + m.group(1)
                    pos = m.end()
                    continue
                nxt = m.start() if m else len(line)
                segment = line[pos:nxt]
                color = self.get_color_pair(fg, self.bg_color)
                self.stdscr.attrset(color)
                if col + len(segment) > self.min_cols:
                    segment = segment[:self.min_cols - col]
                self.stdscr.addstr(y + i, col, segment)
                col += len(segment)
                pos = nxt
            self.stdscr.clrtoeol()
        self.stdscr.attrset(self.get_color_pair(self.fg_color, self.bg_color))

    def wrap_text(self, text, width):
        words = text.split(' ')
        lines = []
        cur = ''
        for w in words:
            if len(cur) + len(w) + 1 > width:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + ' ' + w).strip()
        if cur:
            lines.append(cur)
        return lines
