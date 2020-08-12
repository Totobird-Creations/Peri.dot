##########################################
# DEPENDENCIES                           #
##########################################

from .modules.colorama.colorama import init, Fore, Style # type: ignore
init()

##########################################
# LEX, PARSE, INTERPRET ERRORS           #
##########################################

class Exc_Error():
    def __init__(self, exc, msg, start, end, context):
        self.exc = exc
        self.msg = msg
        self.start = start
        self.end = end
        self.context = context

    def asstring(self):
        result = self.traceback()
        result += f'''   >{Fore.YELLOW}{self.start.lntext}{Style.RESET_ALL}
    {Fore.YELLOW}{' ' * self.start.column}{'^' * (self.end.column - self.start.column)}{Style.RESET_ALL}
{Fore.RED}{Style.BRIGHT}{self.exc}{Style.RESET_ALL}: {Fore.RED}{self.msg}{Style.RESET_ALL}'''
        return(result)

    def traceback(self):
        result = ''
        pos = self.start
        context = self.context

        while context:
            result = f'''  {Fore.GREEN}File {Style.BRIGHT}{pos.file}{Style.RESET_ALL}, {Fore.GREEN}Line {Style.BRIGHT}{pos.line + 1}{Style.RESET_ALL}{Fore.GREEN}, Column {Style.BRIGHT}{pos.column + 1}{Style.RESET_ALL}{Fore.GREEN}, In {Style.BRIGHT}{context.display}{Style.RESET_ALL}\n''' + result

            pos = context.parententry
            context = context.parent

        result = f'{Fore.BLUE}{Style.BRIGHT}Traceback (most recent call last):{Style.RESET_ALL}\n' + result
        return(result)



class Exc_EscapeError(Exc_Error):
    def __init__(self, msg, start, end, context=None):
        super().__init__('EscapeError', msg, start, end, context)

class Exc_IdentifierError(Exc_Error):
    def __init__(self, msg, start, end, context=None):
        super().__init__('IdentifierError', msg, start, end, context)

class Exc_SyntaxError(Exc_Error):
    def __init__(self, msg, start, end, context=None):
        super().__init__('SyntaxError', msg, start, end, context)

class Exc_TypeError(Exc_Error):
    def __init__(self, msg, start, end, context=None):
        super().__init__('TypeError', msg, start, end, context)

class Exc_ValueError(Exc_Error):
    def __init__(self, msg, start, end, context=None):
        super().__init__('ValueError', msg, start, end, context)

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
        result = f'''{Fore.BLUE}{Style.BRIGHT}An error occured while reading arguments{Style.RESET_ALL}
  {Fore.GREEN}Argument{Style.RESET_ALL} {Fore.GREEN}{Style.BRIGHT}{self.argnum}{Style.RESET_ALL}
   >{Fore.YELLOW}{self.arg}{Style.RESET_ALL}
    {Fore.YELLOW}{'^' * len(self.arg)}{Style.RESET_ALL}
{Fore.RED}{Style.BRIGHT}{self.exc}{Style.RESET_ALL}: {Fore.RED}{self.msg}{Style.RESET_ALL}'''
        return(result)

class Cmd_CmdArgumentError(Cmd_CmdError):
    def __init__(self, msg, argnum, arg):
        super().__init__('CmdArgumentError', msg, argnum, arg)

class Cmd_NotSupportedError(Cmd_CmdError):
    def __init__(self, msg, argnum, arg):
        super().__init__('NotSupportedError', msg, argnum, arg)
