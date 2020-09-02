VERSION       = '1.1.2'
MODULEVERSION = '1.1.1'

lang = {
    'exceptions' : {
        'runtimeheader'  : ' RUNTIME ERROR ',
        'runtimefooter'  : '',
        'syntaxheader'   : ' SYNTAX ERROR ',
        'syntaxfooter'   : '',
        'file'           : 'File',
        'module'         : 'Module',
        'in'             : 'In',
        'line'           : 'Line',
        'column'         : 'Column',
        'tracebackheader': 'Traceback (Most recent call last):',

        'argumenterror': {
            'name': 'ArgumentException'
        },
        'attributeerror': {
            'name': 'AttributeException'
        },
        'assertionerror': {
            'name': 'AssertionException'
        },
        'breakerror': {
            'name': 'BreakException',
            'location': 'Can not break from outside loop'
        },
        'continueerror': {
            'name': 'ContinueException',
            'location': 'Can not continue from outside loop'
        },
        'fileaccesserror': {
                'name': 'FileAccessException'
        },
        'identifiererror': {
            'name': 'IdentifierException',
            'notdefined': '\'%s\' is not defined'
        },
        'includeerror': {
            'name': 'IncludeException',
            'failed': 'Failed to include %s:\n  %s \'%s\', %s %s\n%s: %s',
            'doesnotexist': 'Module %s does not exist'
        },
            'indexerror': {
            'name': 'IndexException'
        },
        'iterationerror': {
            'name': 'IterationException',
            'cannot': '%s is not iterable'
        },
        'keyerror': {
            'name': 'KeyException'
        },
        'operationerror': {
            'name': 'OperationException'
        },
        'panicerror': {
            'name': 'PanicException'
        },
        'patternerror': {
            'name': 'PatternException',
            'nomatch': '%s does not match pattern %s'
        },
        'returnerror': {
            'name': 'ReturnException',
            'location': 'Can not return from outside function'
        },
        'reservederror': {
            'name': 'ReservedNameException',
            'reserved': 'Can not assign %s to \'%s\' (reserved)'
        },
        'typeerror': {
            'name': 'TypeException',
            'cannot': '%s of type %s can not %s %s',
            'assigntype': 'Can not assign %s to \'%s\' (%s)',
            'mustbe': '%s must be of type %s, %s given'
        },
        'valueerror': {
            'name': 'ValueException',
            'cannot': '%s of type %s can not %s %s',
        },

        'syntaxerror': {
            'name': 'SyntaxException',
            'illegalchar': 'Illegal character \'%s\' was found',
            'invalideofl': 'Invalid EO%s, expected %s',
            'invalideoflnoexp': 'Invalid EO%s',
            'notfound': 'Expected %s not found'
        },
        'escapeerror': {
            'name': 'EscapeException',
            'cannot': '\'%s\' can not be escaped'
        }
    }
}

def main():
    from .version import catch as catch

    catch.location(f'Peri.dot {VERSION}')
    @catch.catch
    def improvederrormessage():
        ##########################################
        # DEPENDENCIES                           #
        ##########################################

        import sys
        from pathlib import Path

        import click
        from   colorama  import init, Fore, Style
        init()

        from .version import constants          as constants
        from .version import context            as context
        from .version import default            as default
        from .version import exceptions         as exceptions
        from .version import interpreter        as interpreter
        from .version import lexer              as lexer
        from .version import nodes              as nodes
        from .version import parser             as parser
        from .version import repl               as i_repl
        from .version import run                as run
        from .version import tokens             as tokens
        from .version import types              as types
        import perimod

        ##########################################
        # LOGO                                   #
        ##########################################

        def logo() -> str:
            logolines = [
                f'    _____----_____',
                f'   / \ PERI.DOT / \   Peri.dot - {VERSION}',
                f' _/  /\ __     /\  \_  © 2020 Totobird Creations',
                f'/___/  \__\-,  \ \___\ ',
                f'\‾‾‾\ \  \'-\‾‾\  /‾‾‾/ ',
                f' ‾\  \/     ‾‾ \/  /‾  https://github.com/toto-bird/Peri.dot',
                f'   \ / LANGUAGE \ /',
                f'    ‾‾‾‾‾----‾‾‾‾‾'
            ]
            logolength = 0
            for i in range(len(logolines)):
                j = logolines[i]
                if len(j) > logolength:
                    logolength = len(j)
            for i in range(len(logolines)):
                logolines[i] = f' ║ {logolines[i].ljust(logolength, " ")} ║'
            logolines.insert(0, f' ╔{"═" * (logolength + 2)}╗')
            logolines.append(f' ╚{"═" * (logolength + 2)}╝')
            logo = '\n'.join(logolines)
            logo = f'{Fore.GREEN}{Style.BRIGHT}{logo}{Style.RESET_ALL}'
            print(logo, end='\n')
            return(logo)

        ##########################################
        # ARGUMENTS                              #
        ##########################################

        @click.command()
        @click.option('-h', '--help',    is_flag=True)
        @click.option('-v', '--version', is_flag=True)
        @click.option('-r', '--repl',    is_flag=True)
        @click.argument('filename', default='')
        @click.argument('args', nargs=-1)
        def main(help, version, repl, filename, args):
            if version:
                logo()

            if help:
                print(f'''{Fore.YELLOW}Usage{Style.RESET_ALL}: {Fore.YELLOW}{Style.BRIGHT}{Path(sys.argv[0]).name} [OPTIONS]* [FILE]? [ARGS]*{Style.RESET_ALL}

{Fore.BLUE}{Style.BRIGHT}Options:{Style.RESET_ALL}
  {Fore.GREEN}{Style.BRIGHT}-h{Style.RESET_ALL}, {Fore.GREEN}{Style.BRIGHT}--help{Style.RESET_ALL}    - {Fore.GREEN}Display this help message.{Style.RESET_ALL}
  {Fore.GREEN}{Style.BRIGHT}-v{Style.RESET_ALL}, {Fore.GREEN}{Style.BRIGHT}--version{Style.RESET_ALL} - {Fore.GREEN}Display logo and version.{Style.RESET_ALL}
  {Fore.GREEN}{Style.BRIGHT}-r{Style.RESET_ALL}, {Fore.GREEN}{Style.BRIGHT}--repl{Style.RESET_ALL}    - {Fore.GREEN}Enter the repl.{Style.RESET_ALL}''')


            path = str(Path(filename).parent.resolve())

            default._defaultinit(MODULEVERSION, path, types, context)
            exceptions._exceptionsinit(lang)
            interpreter._interpreterinit(lang, tokens, context, default, constants, types, exceptions, run, perimod)
            lexer._lexerinit(lang, constants, tokens, exceptions)
            nodes._nodesinit(types, tokens)
            parser._parserinit(lang, tokens, exceptions, constants, nodes)
            perimod._perimodinit(catch, types, interpreter, exceptions)
            i_repl._replinit(VERSION, default, context, run, lexer, parser, interpreter)
            run._runinit(lexer, parser, context, interpreter)
            types._typesinit(catch, exceptions, context, constants, tokens, nodes, interpreter)

            if filename:
                script = ''

                try:
                    with open(filename, 'r') as f:
                        script = f.read()
                        script = '\n'.join(
                            [
                                i.lstrip(' ').rstrip(' ').lstrip('\t').rstrip('\t') for i in script.split('\n')
                            ]
                        )

                except Exception as e:
                    exc = sys.exc_info()
                    print(exceptions.Cmd_CmdArgumentError(f'{exc[0].__name__}: {str(e)}', 'filename', filename).asstring())
                    exit(1)

                symbols = default.defaultvariables(context.SymbolTable())
                result, exec_context, error = run.run(filename, script, symbols)

                if error:
                    print(error.asstring())
                    exit(1)


            if not (filename or version or help) or repl:
                #print(
                #    Cmd_OutOfDateWarning(f'\n  The REPL is currently out of date and does not have the same functionality as running a file.\n    Proceed with caution as it may crash or have bugs.\n\n    {Style.BRIGHT}PLEASE DO NOT REPORT ANY INTERNAL ERRORS CAUSED BY THE REPL ON GITHUB').asstring()
                #)

                i_repl.PromptToolkitRepl()


        main()

if __name__ == "__main__":
    main()
