import curses
from takoui import TakoApp

def main(stdscr):
    app = TakoApp(stdscr, min_rows=16, min_cols=80, bg_color="#000000", fg_color="#FFFFFF", title="takoui demo")
    app.draw_title()
    options = ["Option 1", "Option 2", "Option 3", "Exit"]
    choice = app.menu(2, 2, options)
    if choice != -1 and options[choice] != "Exit":
        sample_text = "demo of <#ff0000>colored text <#00ff00>preview<#ffffff> in takoui"
        app.preview_text(10, 2, sample_text, 76, 10)
        app.stdscr.getch()

curses.wrapper(main)
