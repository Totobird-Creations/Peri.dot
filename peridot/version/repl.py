##########################################
# DEPENDENCIES                           #
##########################################

import termios, fcntl, sys, os
from .modules.colorama.colorama import init, Fore, Style
init()

from .context     import *
from .default     import *
from .interpreter import *
from .lexer       import *
from .parser      import *

replname = '<repl>'

##########################################
# SINGLE KEYPRESS READER                 #
##########################################

def keypress() -> int:
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK 
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR 
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    try:
        ret = sys.stdin.read(1) # returns a single character
    except KeyboardInterrupt: 
        ret = 0
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return(ord(ret))

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
