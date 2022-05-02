#!/usr/bin/env python3

from curses import wrapper
from functools import partial
import curses
import time


def spd_scale(y0, x0, y1, x1, x):
    """Get the speed at the given value of time.
    NOTE: The output is not clamped,
        regardless of the reference points given."""
    # Two point form of a line
    # y-y0 = y2-y1/x2-x1 (x-x0)
    m = (y1 - y0) / (x1 - x0)
    c = y0
    return c + m * (x - x0)


def main(stdscr):
    """Main loop for listening to input events and displaying speed using curses.
    Takes in the window created by curses.
    Call this function using curses' wrapper function in order to
        not mess up terminal state on exceptions."""

    # Curses Prelude
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)  # Don't show the cursor
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.nodelay(True)  # Don't wait for ENTER to read input
    stdscr.border()

    spd_scale_c = partial(spd_scale, 100, 10, 0, 0)
    w_down_counter = 0
    speed = spd_scale_c(w_down_counter)

    stdscr.attrset(curses.color_pair(1))
    stdscr.addstr(0, curses.COLS // 2, "Motor Control", curses.A_DIM)
    while True:
        keystroke = stdscr.getch()
        if keystroke == ord("q"):
            break
        elif keystroke == ord("w"):
            w_down_counter = min(w_down_counter + 1, 10)
            time.sleep(0.2)
        else:
            w_down_counter = max(w_down_counter - 1, 0)
            time.sleep(0.2)
        speed = spd_scale_c(w_down_counter)
        stdscr.addstr(4, curses.COLS // 2, f"Current speed is {speed}", curses.A_BOLD)
        stdscr.refresh()

    stdscr.refresh()


wrapper(main)
