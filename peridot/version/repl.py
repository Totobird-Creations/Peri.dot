##########################################
# DEPENDENCIES                           #
##########################################

from .modules.colorama.colorama import init, Fore, Style
import curses
init()

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
            text = ''
            pos = 0
            sys.stdout.write(f'{Style.RESET_ALL}{Fore.RED if failed else Fore.GREEN}{Style.BRIGHT}>>> {Style.RESET_ALL}')
            sys.stdout.flush()

            while True:
                key = keypress()

                if key == 4:
                    print(f'{Style.RESET_ALL}\n{Fore.RED}Signal: {Style.BRIGHT}SIGQUIT{Style.RESET_ALL}')
                    end = True
                    break
                elif key == 3:
                    print(f'{Style.RESET_ALL}\n{Fore.RED}Signal: {Style.BRIGHT}SIGINT{Style.RESET_ALL}')
                    break

                elif key == 27: pass
                elif key == 91: pass

                elif key == 8 or key == 127:
                    if pos > 0:
                        text = text[:pos - 1:] + text[pos:]
                        pos -= 1

                elif key == 13:
                    print('')
                    failed = True

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
                                        failed = False

                    print('')
                    break

                else:
                    text = text[:pos:] + chr(key) + text[pos:]
                    pos += 1

                sys.stdout.write(f'{Style.RESET_ALL}\x1b[1F\x1b[1E\x1b[2K{Fore.RED if failed else Fore.GREEN}{Style.BRIGHT}>>> {Style.RESET_ALL}{text}{Style.RESET_ALL}')
                sys.stdout.flush()



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
