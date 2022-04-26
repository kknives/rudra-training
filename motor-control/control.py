#!/usr/bin/env python3

from curses import wrapper
import curses


def main(stdscr):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()

    stdscr.addstr(0, curses.COLS // 2, "Motor Control", curses.A_REVERSE)
    while True:
        keystroke = stdscr.getch()
        if keystroke == ord("q"):
            break

        stdscr.refresh()

    stdscr.refresh()


wrapper(main)
