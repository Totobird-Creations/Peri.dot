##########################################
# DEPENDENCIES                           #
##########################################

import os
from colorama import init, Fore, Style
init()

_HEADER = '\n- RUNTIME ERROR '
_FOOTER = f''

##########################################
# INTERPRETER ERRORS                     #
##########################################

class Exc_Error():
    def __init__(self, exc, msg, start, end, context, originstart=[], originend=[]):
        self.exc = exc
        self.msg = msg
        self.start = start
        self.end = end
        self.context = context
        self.caughterrors = self.context.caughterrors
        self.originstart = originstart
        self.originend = originend


    def fixorigin(self, originstart, originend, indent=-1):
        result = ''
        current = []
        first = True
        originstart = [i for i in originstart if i not in (None, [])] 
        originend   = [i for i in originend   if i not in (None, [])] 
        for i in range(len(originstart)):
            if isinstance(originstart[i], list):
                result += self.fixorigin(originstart[i], originend[i], indent=indent + 1)
                first = False

            else:
                result += f'{Fore.MAGENTA} {" ║" * indent} ╠═{Fore.GREEN}File {Style.BRIGHT}{originstart[i].file}{Style.RESET_ALL}, {Fore.GREEN}In {Style.BRIGHT}UNKNOWN{Style.RESET_ALL}\n'
                result += f'{Fore.MAGENTA} {" ║" * (indent + 1)}   {Fore.GREEN}Line {Style.BRIGHT}{originstart[i].line + 1}{Style.RESET_ALL}, {Fore.GREEN}Column {Style.BRIGHT}{originstart[i].column + 1}{Style.RESET_ALL}\n'
                result += f'{Fore.MAGENTA} {" ║" * (indent + 1)}      {Fore.YELLOW}{Style.BRIGHT}{originstart[i].lntext}{Style.RESET_ALL}\n'
                result += f'{Fore.MAGENTA} {" ║" * (indent + 1)}      {Fore.YELLOW}{" " * originstart[i].column}{"^" * (originend[i].column - originstart[i].column)}{Style.RESET_ALL}\n'
                current.append(i)
                first = False

        if indent == 0:
            return(result)
        else:
            return(result)


    def asstring(self):
        size = os.get_terminal_size()
        result = f'{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{_HEADER}{"-" * max([size[0] - len(_HEADER) + 1, 0])}{Style.RESET_ALL}\n'

        ### CODE FOR SHOWING CAUGHT AND HANDLED ERRORS
        #
        #if len(self.caughterrors) >= 1:
        #    result += f'{Style.RESET_ALL}{Fore.BLUE}{Style.BRIGHT}Caught Errors (Most recent catch last):{Style.RESET_ALL}\n'
        #    for i in range(len(self.caughterrors)):
        #        if not i % 2:
        #            continue
        #        error = self.caughterrors[i]
        #        display = error.context.display
        #        if isinstance(display, tuple):
        #            display = f'{display[0]} <{display[1]}>'
        #
        #        result += f'''  {Fore.GREEN}File {Style.BRIGHT}{error.start.file}{Style.RESET_ALL}, {Fore.GREEN}In {Style.BRIGHT}{display}{Style.RESET_ALL}
#    {Fore.GREEN}Line {Style.BRIGHT}{error.start.line + 1}{Style.RESET_ALL}, {Fore.GREEN}Column {Style.BRIGHT}{error.start.column + 1}{Style.RESET_ALL}\n'''
        #        error.originstart = self.fixorigin(error.originstart)
        #        error.originend = self.fixorigin(error.originend)
        #        for i in range(len(error.originstart)):
        #            result += f'''      {Fore.YELLOW}{Style.BRIGHT}{error.originstart[i].lntext}{Style.RESET_ALL}\n'''
        #            result += f'''      {Fore.YELLOW}{' ' * error.originstart[i].column}{'^' * (error.originend[i].column - error.originstart[i].column)}{Style.RESET_ALL}\n'''
        #        result += f'''      {Fore.YELLOW}{Style.BRIGHT}{error.start.lntext}{Style.RESET_ALL}\n'''
        #        result += f'''      {Fore.YELLOW}{' ' * error.start.column}{'^' * (error.end.column - error.start.column)}{Style.RESET_ALL}\n'''
        #        if error.msg:
        #            result += f'''  {Fore.RED}{Style.BRIGHT}{error.exc}{Style.RESET_ALL}: {Fore.RED}{error.msg}{Style.RESET_ALL}\n'''
        #        else:
        #            result += f'''  {Fore.RED}{Style.BRIGHT}{error.exc}{Style.RESET_ALL}\n'''
        #        result += '\n'
        #    result += f'{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{"-" * size[0]}{Style.RESET_ALL}\n\n'

        result += self.traceback()

        result += self.fixorigin(self.originstart, self.originend)

        display = self.context.display
        if isinstance(display, tuple):
            display = f'{display[0]} <{display[1]}>'

        result += f'  {Fore.GREEN}File {Style.BRIGHT}{self.start.file}{Style.RESET_ALL}, {Fore.GREEN}In {Style.BRIGHT}{display}{Style.RESET_ALL}\n'
        result += f'    {Fore.GREEN}Line {Style.BRIGHT}{self.start.line + 1}{Style.RESET_ALL}, {Fore.GREEN}Column {Style.BRIGHT}{self.start.column + 1}{Style.RESET_ALL}\n'
        result += f'      {Fore.YELLOW}{Style.BRIGHT}{self.start.lntext}{Style.RESET_ALL}\n'
        result += f'      {Fore.YELLOW}{" " * self.start.column}{"^" * (self.end.column - self.start.column)}{Style.RESET_ALL}\n'

        if self.msg:
            result += f'{Fore.RED}{Style.BRIGHT}{self.exc}{Style.RESET_ALL}: {Fore.RED}{self.msg}{Style.RESET_ALL}\n'
        else:
            result += f'{Fore.RED}{Style.BRIGHT}{self.exc}{Style.RESET_ALL}\n'

        result += f'{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{"-" * size[0]}{Style.RESET_ALL}'
        return(result)


    def traceback(self):
        result = ''
        context = self.context.parent
        pos = self.context.parententry

        while context:
            start       = pos[0]
            end         = pos[1]
            result     += self.fixorigin(pos[2], pos[3])

            display = context.display
            if isinstance(display, tuple):
                display = f'{display[0]} <{display[1]}>'

            result += f'  {Fore.GREEN}File {Style.BRIGHT}{start.file}{Style.RESET_ALL}, {Fore.GREEN}In {Style.BRIGHT}{display}{Style.RESET_ALL}\n'
            result += f'    {Fore.GREEN}Line {Style.BRIGHT}{start.line + 1}{Style.RESET_ALL}, {Fore.GREEN}Column {Style.BRIGHT}{start.column + 1}{Style.RESET_ALL}\n'
            result += f'      {Fore.YELLOW}{Style.BRIGHT}{start.lntext}{Style.RESET_ALL}\n'''
            result += f'      {Fore.YELLOW}{" " * start.column}{"^" * (end.column - start.column)}{Style.RESET_ALL}\n'

            pos = context.parententry
            context = context.parent

        result = f'{Style.RESET_ALL}{Fore.BLUE}{Style.BRIGHT}Traceback (Most recent call last):{Style.RESET_ALL}\n{result}'
        return(result)



class Exc_ArgumentError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[]):
        super().__init__('ArgumentException', msg, start, end, context, originstart, originend)

class Exc_ArgumentTypeError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[]):
        super().__init__('ArgTypeException', msg, start, end, context, originstart, originend)

class Exc_AssertionError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[]):
        super().__init__('AssertionException', msg, start, end, context, originstart, originend)

class Exc_FileAccessError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[]):
        super().__init__('FileAccessException', msg, start, end, context, originstart, originend)

class Exc_IdentifierError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[]):
        super().__init__('IdentifierException', msg, start, end, context, originstart, originend)

class Exc_OperationError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[]):
        super().__init__('OperationException', msg, start, end, context, originstart, originend)

class Exc_PanicError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[]):
        super().__init__('PanicException', msg, start, end, context, originstart, originend)

class Exc_ThrowError(Exc_Error):
    def __init__(self, name, msg, start, end, context, originstart=[], originend=[]):
        super().__init__(name, msg, start, end, context, originstart, originend)

class Exc_TypeError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[]):
        super().__init__('TypeException', msg, start, end, context, originstart, originend)

class Exc_ValueError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[]):
        super().__init__('ValueException', msg, start, end, context, originstart, originend)

##########################################
# LEXER, PARSER ERRORS                   #
##########################################

class Syn_Error():
    def __init__(self, exc, msg, start=None, end=None):
        self.exc = exc
        self.msg = msg
        self.start = start
        self.end = end


    def asstring(self):
        result = f'{Style.RESET_ALL}{Fore.BLUE}{Style.BRIGHT}An error occured while lexing and parsing:{Style.RESET_ALL}\n'
        result += f'  {Fore.GREEN}File{Style.RESET_ALL} {Fore.GREEN}{Style.BRIGHT}{self.start.file}{Style.RESET_ALL}\n'
        result += f'    {Fore.GREEN}Line{Style.RESET_ALL} {Fore.GREEN}{Style.BRIGHT}{self.start.line}{Style.RESET_ALL}, {Fore.GREEN}Column{Style.RESET_ALL} {Fore.GREEN}{Style.BRIGHT}{self.start.column}{Style.RESET_ALL}\n'
        result += f'      {Fore.YELLOW}{Style.BRIGHT}{self.start.lntext}{Style.RESET_ALL}\n'
        result += f'      {" " * self.start.column}{Fore.YELLOW}{"^" * (self.end.column - self.start.column)}{Style.RESET_ALL}\n'

        if self.msg:
            result += f'''{Fore.RED}{Style.BRIGHT}{self.exc}{Style.RESET_ALL}: {Fore.RED}{self.msg}{Style.RESET_ALL}'''
        else:
            result += f'''{Fore.RED}{Style.BRIGHT}{self.exc}{Style.RESET_ALL}'''
        return(result)



class Syn_EscapeError(Syn_Error):
    def __init__(self, msg, start, end):
        super().__init__('EscapeException', msg, start, end)

class Syn_SyntaxError(Syn_Error):
    def __init__(self, msg, start, end):
        super().__init__('SyntaxException', msg, start, end)

##########################################
# ARGUMENT ERRORS                        #
##########################################

class Cmd_CmdError():
    def __init__(self, exc, msg, argnum, arg):
        self.exc = exc
        self.msg = msg
        self.argnum = argnum
        self.arg = arg


    def asstring(self):
        result = f'{Fore.BLUE}{Style.BRIGHT}An error occured while reading arguments{Style.RESET_ALL}\n'
        result += f'  {Fore.GREEN}Argument{Style.RESET_ALL} {Fore.GREEN}{Style.BRIGHT}{self.argnum}{Style.RESET_ALL}\n'
        result += f'    {Fore.YELLOW}{self.arg}{Style.RESET_ALL}\n'
        result += f'    {Fore.YELLOW}{"^" * len(self.arg)}{Style.RESET_ALL}\n'
        result += f'{Fore.RED}{Style.BRIGHT}{self.exc}{Style.RESET_ALL}: {Fore.RED}{self.msg}{Style.RESET_ALL}\n'
        return(result)



class Cmd_CmdArgumentError(Cmd_CmdError):
    def __init__(self, msg, argnum, arg):
        super().__init__('CmdArgumentError', msg, argnum, arg)

class Cmd_NotSupportedError(Cmd_CmdError):
    def __init__(self, msg, argnum, arg):
        super().__init__('NotSupportedError', msg, argnum, arg)

##########################################
# CMD WARNINGS                           #
##########################################

class Cmd_CmdWarning():
    def __init__(self, exc, msg):
        self.exc = exc
        self.msg = msg


    def asstring(self):
        result = f'{Fore.RED}{Style.BRIGHT}{self.exc}{Style.RESET_ALL}: {Fore.YELLOW}{self.msg}{Style.RESET_ALL}'
        return(result)



class Cmd_OutOfDateWarning(Cmd_CmdWarning):
    def __init__(self, msg):
        super().__init__('OutOfDateWarning', msg)
