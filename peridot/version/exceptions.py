##########################################
# DEPENDENCIES                           #
##########################################

import os as _os
from colorama import init as _init, Fore as _Fore, Style as _Style
_init()

def _exceptionsinit(conf):
    global lang
    lang = conf

class Exc_BaseException(): pass

##########################################
# INTERPRETER ERRORS                     #
##########################################

class Exc_Error(Exc_BaseException):
    def __init__(self, exc, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        self.exc = exc
        self.msg = msg
        self.start = start
        self.end = end
        self.context = context
        #self.caughterrors = self.context.caughterrors
        self.originstart = originstart
        self.originend = originend
        self.origindisplay = origindisplay


    def fixorigin(self, origin, first=True):
        try:
            origin = [i for i in origin if i not in (None, [])] 
        except TypeError:
            return([origin])
        result = []

        if not first and len(origin) == 0:
            return(None)

        for i in range(len(origin)):
            org = origin[i]

            if isinstance(org, list):
                f = self.fixorigin(org, first)
                if f:
                    result.append(f)
            else:
                if not first and len(origin) == 1:
                    return(org)
                result.append(org)

        return(result)



    def formatorigin(self, originstart, originend, origindisplay, indent=0, ignore=[]):
        result = []
        originstart.reverse()
        originend.reverse()
        origindisplay.reverse()

        prefix = ''
        for i in ignore:
            if i:
                prefix += '  '
            else:
                prefix += '║ '

        index = 0
        for i in range(len(originstart)):
            orgstart   = originstart[i]
            orgend     = originend[i]
            orgdisplay = origindisplay[i]
            l = [i for i in originstart if not isinstance(i, list)]

            if isinstance(orgstart, list):
                if index > len(l) - 1:
                    ig = ignore + [True]
                else:
                    ig = ignore + [False]
                result += self.formatorigin(orgstart, orgend, orgdisplay, indent + 1, ig)

            else:
                if index >= len(l) - 1:
                    cornertype = '╔'
                else:
                    cornertype = '╠'
                display = self.context.display
                if isinstance(display, tuple):
                    display = f'{display[0]} <{display[1]}>'
                result.append(f'  {_Fore.MAGENTA}{prefix}║     {_Fore.YELLOW}{" " * (orgstart.column)}{"^" * (orgend.column - orgstart.column)}{_Style.RESET_ALL}')
                result.append(f'  {_Fore.MAGENTA}{prefix}║     {_Fore.YELLOW}{_Style.BRIGHT}{orgstart.lntext}{_Style.RESET_ALL}')
                result.append(f'  {_Fore.MAGENTA}{prefix}║   {_Fore.GREEN}{lang["exceptions"]["line"]} {_Style.BRIGHT}{orgstart.line + 1}{_Style.RESET_ALL} {_Fore.GREEN}{lang["exceptions"]["column"]} {_Style.BRIGHT}{orgstart.column + 1}{_Style.RESET_ALL}')
                result.append(f'  {_Fore.MAGENTA}{prefix}{cornertype}═{_Fore.GREEN}{lang["exceptions"]["file"]} {_Style.BRIGHT}{orgstart.file}{_Style.RESET_ALL}, {_Fore.GREEN}{lang["exceptions"]["in"]} {_Style.BRIGHT}{display}{_Style.RESET_ALL}')
                index += 1
        
        if indent == 0:
            result.reverse()
            result = '\n'.join(result) + '\n'
        return(result)


    def asstring(self):
        size = _os.get_terminal_size()
        result = f'{_Style.RESET_ALL}{_Fore.RED}{_Style.BRIGHT}-{lang["exceptions"]["runtimeheader"]}{"-" * max([size[0] - len(lang["exceptions"]["runtimeheader"]) - 1, 0])}{_Style.RESET_ALL}\n'

        ### CODE FOR SHOWING CAUGHT AND HANDLED ERRORS
        #
        #if len(self.caughterrors) >= 1:
        #    result += f'{_Style.RESET_ALL}{_Fore.BLUE}{_Style.BRIGHT}Caught Errors (Most recent catch last):{_Style.RESET_ALL}\n'
        #    for i in range(len(self.caughterrors)):
        #        if not i % 2:
        #            continue
        #        error = self.caughterrors[i]
        #        display = error.context.display
        #        if isinstance(display, tuple):
        #            display = f'{display[0]} <{display[1]}>'
        #
        #        result += f'''  {_Fore.GREEN}File {_Style.BRIGHT}{error.start.file}{_Style.RESET_ALL}, {_Fore.GREEN}In {_Style.BRIGHT}{display}{_Style.RESET_ALL}
#    {_Fore.GREEN}Line {_Style.BRIGHT}{error.start.line + 1}{_Style.RESET_ALL}, {_Fore.GREEN}Column {_Style.BRIGHT}{error.start.column + 1}{_Style.RESET_ALL}\n'''
        #        error.originstart = self.fixorigin(error.originstart)
        #        error.originend = self.fixorigin(error.originend)
        #        for i in range(len(error.originstart)):
        #            result += f'''      {_Fore.YELLOW}{_Style.BRIGHT}{error.originstart[i].lntext}{_Style.RESET_ALL}\n'''
        #            result += f'''      {_Fore.YELLOW}{' ' * error.originstart[i].column}{'^' * (error.originend[i].column - error.originstart[i].column)}{_Style.RESET_ALL}\n'''
        #        result += f'''      {_Fore.YELLOW}{_Style.BRIGHT}{error.start.lntext}{_Style.RESET_ALL}\n'''
        #        result += f'''      {_Fore.YELLOW}{' ' * error.start.column}{'^' * (error.end.column - error.start.column)}{_Style.RESET_ALL}\n'''
        #        if error.msg:
        #            result += f'''  {_Fore.RED}{_Style.BRIGHT}{error.exc}{_Style.RESET_ALL}: {_Fore.RED}{error.msg}{_Style.RESET_ALL}\n'''
        #        else:
        #            result += f'''  {_Fore.RED}{_Style.BRIGHT}{error.exc}{_Style.RESET_ALL}\n'''
        #        result += '\n'
        #    result += f'{_Style.RESET_ALL}{_Fore.RED}{_Style.BRIGHT}{"-" * size[0]}{_Style.RESET_ALL}\n\n'

        result += self.traceback()

        self.originstart = self.fixorigin(self.originstart)
        if not self.originstart:
            self.originstart = []
            self.originend = []
            self.origindisplay = []
        else:
            self.originend = self.fixorigin(self.originend)
            self.origindisplay = self.fixorigin(self.origindisplay)
        result += self.formatorigin(self.originstart, self.originend, self.origindisplay)

        display = self.context.display
        if isinstance(display, tuple):
            display = f'{display[0]} <{display[1]}>'

        result += f'  {_Fore.GREEN}{lang["exceptions"]["file"]} {_Style.BRIGHT}{self.start.file}{_Style.RESET_ALL}, {_Fore.GREEN}{lang["exceptions"]["in"]} {_Style.BRIGHT}{display}{_Style.RESET_ALL}\n'
        result += f'    {_Fore.GREEN}{lang["exceptions"]["line"]} {_Style.BRIGHT}{self.start.line + 1}{_Style.RESET_ALL}, {_Fore.GREEN}{lang["exceptions"]["column"]} {_Style.BRIGHT}{self.start.column + 1}{_Style.RESET_ALL}\n'
        result += f'      {_Fore.YELLOW}{_Style.BRIGHT}{self.start.lntext}{_Style.RESET_ALL}\n'
        result += f'      {_Fore.YELLOW}{" " * self.start.column}{"^" * (self.end.column - self.start.column)}{_Style.RESET_ALL}\n'

        if self.msg:
            result += f'\n{_Fore.RED}{_Style.BRIGHT}{self.exc}{_Style.RESET_ALL}: {_Fore.RED}{self.msg}{_Style.RESET_ALL}\n'
        else:
            result += f'\n{_Fore.RED}{_Style.BRIGHT}{self.exc}{_Style.RESET_ALL}\n'

        result += f'{_Style.RESET_ALL}{_Fore.RED}{_Style.BRIGHT}-{lang["exceptions"]["runtimefooter"]}{"-" * max([size[0] - len(lang["exceptions"]["runtimefooter"]) - 1, 0])}{_Style.RESET_ALL}\n'
        return(result)


    def traceback(self):
        result = ''
        context = self.context.parent
        pos = self.context.parententry

        while context:
            start       = pos[0]
            end         = pos[1]

            try:
                pos[2] = pos[2][0]
                pos[3] = pos[3][0]
                pos[4] = pos[4][0]
            except IndexError: pass

            pos[2] = self.fixorigin(pos[2])
            pos[3] = self.fixorigin(pos[3])
            pos[4] = self.fixorigin(pos[4])
            result     += self.formatorigin(pos[2], pos[3], pos[4])

            display = context.display
            if isinstance(display, tuple):
                display = f'{display[0]} <{display[1]}>'

            result += f'  {_Fore.GREEN}{lang["exceptions"]["file"]} {_Style.BRIGHT}{start.file}{_Style.RESET_ALL}, {_Fore.GREEN}{lang["exceptions"]["in"]} {_Style.BRIGHT}{display}{_Style.RESET_ALL}\n'
            result += f'    {_Fore.GREEN}{lang["exceptions"]["line"]} {_Style.BRIGHT}{start.line + 1}{_Style.RESET_ALL}, {_Fore.GREEN}{lang["exceptions"]["column"]} {_Style.BRIGHT}{start.column + 1}{_Style.RESET_ALL}\n'
            result += f'      {_Fore.YELLOW}{_Style.BRIGHT}{start.lntext}{_Style.RESET_ALL}\n'''
            result += f'      {_Fore.YELLOW}{" " * start.column}{"^" * (end.column - start.column)}{_Style.RESET_ALL}\n'

            pos = context.parententry
            context = context.parent

        result = f'{_Style.RESET_ALL}{_Fore.BLUE}{_Style.BRIGHT}{lang["exceptions"]["tracebackheader"]}{_Style.RESET_ALL}\n{result}'
        return(result)



class Exc_ArgumentError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["argumenterror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_AttributeError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["attributeerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_AssertionError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["assertionerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_BreakError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["breakerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_ContinueError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["continueerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_FileAccessError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["fileaccesserror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_IdentifierError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["identifiererror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_IncludeError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["includeerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_IndexError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["indexerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_IterationError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["iterationerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_KeyError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["keyerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_OperationError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["operationerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_PanicError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["panicerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_PatternError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["patternerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_ReservedError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["reservederror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_ReturnError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["returnerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_ThrowError(Exc_Error):
    def __init__(self, name, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(name, msg, start, end, context, originstart, originend, origindisplay)

class Exc_TypeError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["typeerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)

class Exc_ValueError(Exc_Error):
    def __init__(self, msg, start, end, context, originstart=[], originend=[], origindisplay=[]):
        super().__init__(f'{lang["exceptions"]["valueerror"]["name"]}', msg, start, end, context, originstart, originend, origindisplay)



##########################################
# LEXER, PARSER ERRORS                   #
##########################################

class Syn_Error(Exc_BaseException):
    def __init__(self, exc, msg, start=None, end=None):
        self.exc = exc
        self.msg = msg
        self.start = start
        self.end = end


    def asstring(self):
        size = _os.get_terminal_size()
        result = f'{_Style.RESET_ALL}{_Fore.RED}{_Style.BRIGHT}-{lang["exceptions"]["syntaxheader"]}{"-" * max([size[0] - len(lang["exceptions"]["syntaxheader"]) - 1, 0])}{_Style.RESET_ALL}\n'
        result += f'{_Style.RESET_ALL}{_Fore.BLUE}{_Style.BRIGHT}An error occured while lexing and parsing:{_Style.RESET_ALL}\n'
        result += f'  {_Fore.GREEN}File{_Style.RESET_ALL} {_Fore.GREEN}{_Style.BRIGHT}{self.start.file}{_Style.RESET_ALL}\n'
        result += f'    {_Fore.GREEN}Line{_Style.RESET_ALL} {_Fore.GREEN}{_Style.BRIGHT}{self.start.line + 1}{_Style.RESET_ALL}, {_Fore.GREEN}Column{_Style.RESET_ALL} {_Fore.GREEN}{_Style.BRIGHT}{self.start.column + 1}{_Style.RESET_ALL}\n'
        result += f'      {_Fore.YELLOW}{_Style.BRIGHT}{self.start.lntext}{_Style.RESET_ALL}\n'
        result += f'      {" " * self.start.column}{_Fore.YELLOW}{"^" * (self.end.column - self.start.column)}{_Style.RESET_ALL}\n'

        if self.msg:
            result += f'''{_Fore.RED}{_Style.BRIGHT}{self.exc}{_Style.RESET_ALL}: {_Fore.RED}{self.msg}{_Style.RESET_ALL}'''
        else:
            result += f'''{_Fore.RED}{_Style.BRIGHT}{self.exc}{_Style.RESET_ALL}'''

        result += f'{_Style.RESET_ALL}\n{_Fore.RED}{_Style.BRIGHT}-{lang["exceptions"]["syntaxfooter"]}{"-" * max([size[0] - len(lang["exceptions"]["syntaxfooter"]) - 1, 0])}{_Style.RESET_ALL}\n'

        return(result)



class Syn_EscapeError(Syn_Error):
    def __init__(self, msg, start, end):
        super().__init__(lang['exceptions']['escapeerror']['name'], msg, start, end)

class Syn_SyntaxError(Syn_Error):
    def __init__(self, msg, start, end):
        super().__init__(lang['exceptions']['syntaxerror']['name'], msg, start, end)

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
        result = f'{_Fore.BLUE}{_Style.BRIGHT}An error occured while reading arguments{_Style.RESET_ALL}\n'
        result += f'  {_Fore.GREEN}Argument{_Style.RESET_ALL} {_Fore.GREEN}{_Style.BRIGHT}{self.argnum}{_Style.RESET_ALL}\n'
        result += f'    {_Fore.YELLOW}{self.arg}{_Style.RESET_ALL}\n'
        result += f'    {_Fore.YELLOW}{"^" * len(self.arg)}{_Style.RESET_ALL}\n'
        result += f'{_Fore.RED}{_Style.BRIGHT}{self.exc}{_Style.RESET_ALL}: {_Fore.RED}{self.msg}{_Style.RESET_ALL}\n'
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

class Cmd_CmdWarning(Exc_BaseException):
    def __init__(self, exc, msg):
        self.exc = exc
        self.msg = msg


    def asstring(self):
        result = f'{_Fore.RED}{_Style.BRIGHT}{self.exc}{_Style.RESET_ALL}: {_Fore.YELLOW}{self.msg}{_Style.RESET_ALL}'
        return(result)



class Cmd_OutOfDateWarning(Cmd_CmdWarning):
    def __init__(self, msg):
        super().__init__('OutOfDateWarning', msg)
