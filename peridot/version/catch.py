import os as _os
from traceback import format_exc as _format_exc
from colorama import init as _init, Fore as _Fore, Style as _Style
_init()

class InternalPeridotError(BaseException): pass

_HEADER = '\n- INTERNAL ERROR '
_FOOTER = f'{_Fore.BLUE}{_Style.BRIGHT}Please report this error on github\n  (https://github.com/toto-bird/Peri.dot/issues/new){_Style.RESET_ALL}'

def catch(func):
    try:
        func()



    except Exception as e:
        size = _os.get_terminal_size()
        traceback = _format_exc()
        print(f'{_Style.RESET_ALL}{_Fore.RED}{_Style.BRIGHT}{_HEADER}{"-" * max([size[0] - len(_HEADER) + 1, 0])}{_Style.RESET_ALL}\n')

        traceback = traceback.rstrip('\n').split('\n\n')
        traceback = [i.split('\n') for i in traceback]

        for j in range(len(traceback)):
            lines = traceback[j]

            for i in range(len(lines)):
                ln = lines[i]


                if ln == 'During handling of the above exception, another exception occurred:':
                    print(f'{_Fore.RED}{_Style.BRIGHT}{ln}{_Style.RESET_ALL}')

                elif i == len(lines) - 1:
                    ln = ln.split(' ')
                    ln = [ln[0][:-1], ' '.join(ln[1:])]
                    print(f'{_Fore.RED}{_Style.BRIGHT}{ln[0]}{_Style.RESET_ALL}: {_Fore.RED}{ln[1]}{_Style.RESET_ALL}')

                elif ln == 'Traceback (most recent call last):':
                    print(f'{_Fore.RED}{_Style.BRIGHT}{ln}{_Style.RESET_ALL}')

                elif ln.startswith('    '):
                    ln = ln.lstrip(' ')
                    print(f'      {_Style.BRIGHT}{ln}{_Style.RESET_ALL}')

                elif ln.startswith('  '):
                    ln = ln.lstrip(' ').split(' ')
                    ln = [ln[1][1:-2], ln[-3][:-1], ln[-1]]
                    print(f'  {_Fore.RED}File {_Style.BRIGHT}\'{ln[0]}\'{_Style.RESET_ALL}')
                    print(f'    {_Fore.RED}Line {_Style.BRIGHT}{ln[1]}{_Style.RESET_ALL} {_Fore.RED}In {_Style.BRIGHT}{ln[2]}{_Style.RESET_ALL}')

                else:
                    print(ln)


            if j < len(traceback) - 1:
                print('')


        print(f'\n{_Style.RESET_ALL}{_Fore.RED}{_Style.BRIGHT}{"-" * size[0]}{_Style.RESET_ALL}')
        print(f'{_FOOTER}')
        print(f'{_Style.RESET_ALL}{_Fore.RED}{_Style.BRIGHT}{"-" * size[0]}{_Style.RESET_ALL}')



    except InternalPeridotError as e:
        size = _os.get_terminal_size()
        traceback = _format_exc()
        print(f'{_Style.RESET_ALL}{_Fore.RED}{_Style.BRIGHT}{_HEADER}{"-" * max([size[0] - len(_HEADER) + 1, 0])}{_Style.RESET_ALL}')

        traceback = traceback.rstrip('\n').split('\n\n')
        traceback = [i.split('\n') for i in traceback]

        for j in range(len(traceback)):
            lines = traceback[j]

            for i in range(len(lines)):
                ln = lines[i]


                if ln == 'During handling of the above exception, another exception occurred:':
                    print(f'{_Fore.RED}{_Style.BRIGHT}{ln}{_Style.RESET_ALL}')

                elif i == len(lines) - 1:
                    ln = ln.split(' ')
                    ln = [ln[0][:-1], ' '.join(ln[1:])]
                    print(f'{_Fore.RED}{_Style.BRIGHT}{ln[0]}{_Style.RESET_ALL}: {_Fore.RED}{ln[1]}{_Style.RESET_ALL}')

                elif ln == 'Traceback (most recent call last):':
                    print(f'{_Fore.RED}{_Style.BRIGHT}{ln}{_Style.RESET_ALL}')

                elif ln.startswith('    '):
                    ln = ln.lstrip(' ')
                    print(f'      {_Style.BRIGHT}{ln}{_Style.RESET_ALL}')

                elif ln.startswith('  '):
                    ln = ln.lstrip(' ').split(' ')
                    ln = [ln[1][1:-2], ln[-3][:-1], ln[-1]]
                    print(f'  {_Fore.RED}File {_Style.BRIGHT}\'{ln[0]}\'{_Style.RESET_ALL}')
                    print(f'    {_Fore.RED}Line {_Style.BRIGHT}{ln[1]}{_Style.RESET_ALL} {_Fore.RED}In {_Style.BRIGHT}{ln[2]}{_Style.RESET_ALL}')

                else:
                    print(ln)


            if j < len(traceback) - 1:
                print('')


        print(f'{_Style.RESET_ALL}{_Fore.RED}{_Style.BRIGHT}{"-" * size[0]}{_Style.RESET_ALL}')
        print(f'{_FOOTER}')
        print(f'{_Style.RESET_ALL}{_Fore.RED}{_Style.BRIGHT}{"-" * size[0]}{_Style.RESET_ALL}')
