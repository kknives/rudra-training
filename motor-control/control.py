#!/usr/bin/env python3

from curses import wrapper
from functools import partial
import curses


def spd_scale(y0, x0, y1, x1, x):
    # y-y0 = y2-y1/x2-x1 (x-x0)
    return y0 + ((y1 - y0) * x / (x1 - x0))


def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.nodelay(True)

    spd_scale_c = partial(spd_scale, 100, 10, 0, 0)
    w_down_counter = 0
    speed = spd_scale_c(w_down_counter)

    stdscr.addstr(0, curses.COLS // 2, "Motor Control", curses.A_REVERSE)
    while True:
        keystroke = stdscr.getch()
        if keystroke == ord("q"):
            break
        elif keystroke == ord("w"):
            w_down_counter = min(w_down_counter + 1, 100)
        else:
            w_down_counter = max(w_down_counter - 1, 0)
        speed = spd_scale_c(w_down_counter)
        stdscr.addstr(
            4, curses.COLS // 2, f"Current speed is {speed}", curses.A_REVERSE
        )
        stdscr.refresh()

    stdscr.refresh()


wrapper(main)
