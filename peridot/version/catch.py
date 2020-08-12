import os
from traceback import format_exc
from .modules.colorama.colorama import init, Fore, Style
init()

_HEADER = '\n- INTERNAL ERROR '
_FOOTER = f'{Fore.BLUE}{Style.BRIGHT}Please report this error on github\n  (https://github.com/toto-bird/Peri.dot/issues/new){Style.RESET_ALL}'

def catch(func):
    try:
        func()
    except Exception as e:
        size = os.get_terminal_size()
        traceback = format_exc()
        print(f'{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{_HEADER}{"-" * max([size[0] - len(_HEADER), 0])}{Style.RESET_ALL}')

        traceback = traceback.rstrip('\n').split('\n\n')
        traceback = [i.split('\n') for i in traceback]

        for j in range(len(traceback)):
            lines = traceback[j]

            for i in range(len(lines)):
                ln = lines[i]


                if ln == 'During handling of the above exception, another exception occurred:':
                    print(f'{Fore.BLUE}{Style.BRIGHT}{ln}{Style.RESET_ALL}')

                elif i == len(lines) - 1:
                    ln = ln.split(' ')
                    ln = [ln[0][:-1], ' '.join(ln[1:])]
                    print(f'{Fore.RED}{Style.BRIGHT}{ln[0]}{Style.RESET_ALL}: {Fore.RED}{ln[1]}{Style.RESET_ALL}')

                elif ln == 'Traceback (most recent call last):':
                    print(f'{Fore.BLUE}{Style.BRIGHT}{ln}{Style.RESET_ALL}')

                elif ln.startswith('    '):
                    ln = ln.lstrip(' ')
                    print(f'      {Fore.YELLOW}{Style.BRIGHT}{ln}{Style.RESET_ALL}')

                elif ln.startswith('  '):
                    ln = ln.lstrip(' ').split(' ')
                    ln = [ln[1][1:-2], ln[-3][:-1], ln[-1]]
                    print(f'  {Fore.GREEN}File {Style.BRIGHT}\'{ln[0]}\'{Style.RESET_ALL}')
                    print(f'    {Fore.GREEN}Line {Style.BRIGHT}{ln[1]}{Style.RESET_ALL} {Fore.GREEN}In {Style.BRIGHT}{ln[2]}{Fore.GREEN}{Style.RESET_ALL}')

                else:
                    print(ln)


            if j < len(traceback) - 1:
                print('')


        print(f'{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{"-" * size[0]}{Style.RESET_ALL}')
        print(f'{_FOOTER}')
        print(f'{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{"-" * size[0]}{Style.RESET_ALL}')