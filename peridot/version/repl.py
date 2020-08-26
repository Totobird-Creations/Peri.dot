##########################################
# DEPENDENCIES                           #
##########################################

def _replinit(default, context, runu):
    global defaultvariables
    defaultvariables = default.defaultvariables
    global SymbolTable
    SymbolTable      = context.SymbolTable
    global run
    run              = runu.run


##########################################
# REPL                                   #
##########################################

replname = '<repl>'

class Repl():
    def __init__(self):
        end = False
        symbols = defaultvariables(SymbolTable())
        failed = False

        while not end:
            script = input('>>> ')

            result, context, error = run(replname, script, symbols)

            if error:
                print(error.asstring())

            if result:
                print('\n'.join(str(i) for i in result))

            print('')



#class CursesRepl():
#    def __init__(self):
#        curses.wrapper(self.main)
#
#    def main(self, stdscr):
#        if curses.can_change_color():
#            curses.init_color(0, 0, 0, 0)
#
#        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
#        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
#
#        stdscr.clear()
#
#        while True:
#            try:
#                size = stdscr.getmaxyx()
#                if size[0] >= 2:
#                    stdscr.addstr(
#                        0, 0,
#                        TITLE.center(size[1], ' '),
#                        curses.color_pair(1) | curses.A_REVERSE | curses.A_BOLD
#                    )
#                if size[0] >= 1:
#                    stdscr.insstr(
#                        size[0] - 1, 0,
#                        TITLE.center(size[1], ' '),
#                        curses.color_pair(2) | curses.A_REVERSE
#                    )
#
#                stdscr.refresh()
#
#            except KeyboardInterrupt as e:
#                raise KeyboardInterrupt(str(e))
