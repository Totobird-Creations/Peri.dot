VERSION = '1.0.0'

if __name__ == "__main__":
    import peridot.version.catch as catch

    catch.location(f'Periscope {VERSION}')
    @catch.catch
    def improvederrormessage():
        ##########################################
        # DEPENDENCIES                           #
        ##########################################

        import sys

        import click
        from   colorama                    import init, Fore, Style
        from   pathlib                     import Path
        init()

        from peridot.__main__              import lang, MODULEVERSION
        import peridot.version.catch       as catch
        import peridot.version.constants   as constants
        import peridot.version.context     as context
        import peridot.version.default     as default
        import peridot.version.exceptions  as exceptions
        import peridot.version.interpreter as interpreter
        import peridot.version.lexer       as lexer
        import peridot.version.nodes       as nodes
        import peridot.version.parser      as parser
        import peridot.version.run         as run
        import peridot.version.tokens      as tokens
        import peridot.version.types       as types
        import perimod

        default._defaultinit(MODULEVERSION, str(Path(__file__).parent), types, context)
        exceptions._exceptionsinit(lang)
        interpreter._interpreterinit(lang, tokens, context, default, constants, types, exceptions, run, perimod)
        lexer._lexerinit(lang, constants, tokens, exceptions)
        nodes._nodesinit(types, tokens)
        parser._parserinit(lang, tokens, exceptions, constants, nodes)
        perimod._perimodinit(catch, types, interpreter, exceptions)
        run._runinit(lexer, parser, context, interpreter)
        types._typesinit(catch, exceptions, context, constants, tokens, nodes, interpreter)

        from   .version                    import test

        test._testinit(run, interpreter, perimod, default, context, types, exceptions)

        ##########################################
        # LOGO                                   #
        ##########################################

        def logo() -> str:
            logolines = [
                f'    _____----_____',
                f'   / \   PERI   / \   Periscope - {VERSION}',
                f' _/  /\  ____  /\  \_  © 2020 Totobird Creations',
                f'/___/ / / __ \/  \___\ ',
                f'\‾‾‾\  /\ ‾‾ / / /‾‾‾/ ',
                f' ‾\  \/  ‾‾‾‾  \/  /‾  https://github.com/toto-bird/Peri.dot',
                f'   \ /  SC()PE  \ /',
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
            logo = f'{Fore.CYAN}{Style.BRIGHT}{logo}{Style.RESET_ALL}'
            print(logo, end='\n')
            return(logo)

        ##########################################
        # ARGUMENTS                              #
        ##########################################

        @click.command()
        @click.option('-h', '--help',    is_flag=True)
        @click.option('-v', '--version', is_flag=True)
        @click.argument('files', nargs=-1)
        def main(help, version, files):
            if version:
                logo()

            if help:
                print(f'''{Fore.MAGENTA}Usage{Style.RESET_ALL}: {Fore.MAGENTA}{Style.BRIGHT}{Path(sys.argv[0]).name} [OPTIONS]* [FILE]? [ARGS]*{Style.RESET_ALL}

{Fore.BLUE}{Style.BRIGHT}Options:{Style.RESET_ALL}
  {Fore.CYAN}{Style.BRIGHT}-h{Style.RESET_ALL}, {Fore.CYAN}{Style.BRIGHT}--help{Style.RESET_ALL}    - {Fore.CYAN}Display this help message.{Style.RESET_ALL}
  {Fore.CYAN}{Style.BRIGHT}-v{Style.RESET_ALL}, {Fore.CYAN}{Style.BRIGHT}--version{Style.RESET_ALL} - {Fore.CYAN}Display logo and version.{Style.RESET_ALL}''')


            if files:
                scripts = []
                
                for i in files:
                    try:
                        with open(i, 'r') as f:
                            script = f.read()
                            scripts.append(('\n'.join(
                                [
                                    i.lstrip(' ').rstrip(' ').lstrip('\t').rstrip('\t') for i in script.split('\n')
                                ]
                            ), i))

                    except Exception as e:
                        exc = sys.exc_info()
                        print(exceptions.Cmd_CmdArgumentError(f'{exc[0].__name__}: {str(e)}', 'filename', i).asstring())
                        exit(1)

                result = test.test(scripts)

                if result:
                    exit(1)
                else:
                    exit(0)

        main()