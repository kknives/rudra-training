#!/usr/bin/env python3

from curses import wrapper
import curses


def main(stdscr):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()

    stdscr.addstr(0, 0, "Motor Control", curses.A_REVERSE)

    stdscr.refresh()
    stdscr.getkey()


wrapper(main)
