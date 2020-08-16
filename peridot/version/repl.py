##########################################
# DEPENDENCIES                           #
##########################################

import sys

from .context     import *
from .default     import *
from .interpreter import *
from .lexer       import *
from .parser      import *

replname = '<repl>'

##########################################
# REPL                                   #
##########################################

class Repl():
    def __init__(self):
        end = False
        symbols = defaultvariables(SymbolTable())
        failed = False

        while not end:
            text = input('>>> ')

            lexer = Lexer('<repl>', text)
            tokens, error = lexer.maketokens()

            if error:
                print(error.asstring)

            else:
                if len(tokens) - 2:
                    parser = Parser(tokens)
                    ast = parser.parse()

                    if ast.error:
                        print(ast.error.asstring())

                    else:
                        context = Context('<file>', symbols=symbols)

                        for i in ast.node:
                            interpreter = Interpreter()
                            result = interpreter.visit(i, context)

                            if result.error:
                                print(result.error.asstring())

                            else:
                                print(result.value)

            print('')
            break



class CursesRepl():
    def __init__(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        if curses.can_change_color():
            curses.init_color(0, 0, 0, 0)

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

        stdscr.clear()

        while True:
            try:
                size = stdscr.getmaxyx()
                if size[0] >= 2:
                    stdscr.addstr(
                        0, 0,
                        TITLE.center(size[1], ' '),
                        curses.color_pair(1) | curses.A_REVERSE | curses.A_BOLD
                    )
                if size[0] >= 1:
                    stdscr.insstr(
                        size[0] - 1, 0,
                        TITLE.center(size[1], ' '),
                        curses.color_pair(2) | curses.A_REVERSE
                    )

                stdscr.refresh()

            except KeyboardInterrupt as e:
                raise KeyboardInterrupt(str(e))
