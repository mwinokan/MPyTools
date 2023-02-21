#!/usr/bin/env python3

import curses
stdscr = curses.initscr()
curses.echo()
curses.nocbreak()
curses.curs_set(1)
stdscr.keypad(False)
curses.endwin()
