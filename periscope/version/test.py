from colorama import init, Fore, Style
init()
from os import get_terminal_size
from datetime import datetime

from prompt_toolkit                                   import print_formatted_text
from prompt_toolkit.shortcuts                         import ProgressBar
from prompt_toolkit.formatted_text                    import HTML
from prompt_toolkit.shortcuts.progress_bar.formatters import *
from prompt_toolkit.styles                            import Style as pStyle
from prompt_toolkit.output.color_depth                import ColorDepth
from time import sleep

from xml.sax.saxutils                                 import escape

def _testinit(runu, interpreter, perimodu, default, context, types, exceptions):
    global run
    run = runu.run
    global RTResult
    RTResult = interpreter.RTResult
    global perimod
    perimod = perimodu
    global defaultvariables
    defaultvariables = default.defaultvariables
    global SymbolTable, Context
    SymbolTable = context.SymbolTable
    Context = context.Context
    global TypeObj
    TypeObj = types.TypeObj
    global Exc_BaseException, Exc_ReturnError
    Exc_BaseException = exceptions.Exc_BaseException
    Exc_ReturnError = exceptions.Exc_ReturnError

    symbols = defaultvariables(SymbolTable())
    perimod._context = Context('<file>', symbols, context, [None, None, None, None, None])
    perimod._symbols = symbols
    perimod._position = TypeObj().setpos(None, None).setcontext(perimod._context)
    perimod._file = 'periscope'
    global periscope
    from peridot.version.modules import periscope



def pprint(format, style=None, color_depth=None):
    print_formatted_text(HTML(format), style=style, color_depth=color_depth)



def test(scripts):
    starttime = datetime.now()



    tests = []
    for i in scripts:
        symbols = defaultvariables(SymbolTable())
        result, exec_context, error = run(i[1], i[0], symbols)

        symbols = {key:value for (key, value) in symbols.symbols.items() if key.startswith('pscope_')}

        if error:
            if isinstance(error, Exc_ReturnError):
                if isinstance(error.returnvalue, periscope.PeriSkip):
                    tests.append((i[1], symbols, error.returnvalue))
                else:
                    tests.append((i[1], symbols, error))
            else:
                tests.append((i[1], symbols, error))
        else:
            tests.append((i[1], symbols))

    totaltests = sum([len(i[1]) for i in tests])

    style = pStyle.from_dict({
        'label'      : 'ansiblue bold',
        'percborder' : 'ansiyellow',
        'percentage' : 'ansiyellow bold',
        'current'    : 'ansiyellow bold',
        'total'      : 'ansiyellow bold',
        'totaltime'  : 'ansiyellow bold',
        'bar'        : 'ansigreen',
    })



    size = get_terminal_size()
    text = ' Testing Started '
    left = '═' * (int(size[0] / 2) - int(len(text) / 2))
    right = '═' * (size[0] - len(text) - len(left))
    pprint(f'\n{escape(left)}<bold>{escape(text)}</bold>{escape(right)}\n', style=style)

    formatters = [
        Text(' '),
        Label(),
        Text(': '),
        Text('[', style='class:percborder'),
        Percentage(),
        Text('][', style='class:percborder'),
        Progress(),
        Text('] ', style='class:percborder'),
        Bar(sym_a='#', sym_b='#', sym_c='-'),
        #Text(' eta [', style='class:percborder'),
        #TimeLeft(),
        #Text('] ', style='class:percborder')
        Text(' ')
    ]

    overview = []
    summary  = []
    errors   = []
    failed = 0
    synfailed = False
    passed = 0

    with ProgressBar(style=style, formatters=formatters, title=HTML(f'<ansigreen>Tracking <bold>{totaltests}</bold> tests...</ansigreen>')) as pb:
        for i in tests:
            if len(i) >= 3:
                if isinstance(i[2], Exc_BaseException):
                    overview.append((i[0], [('fail', i[2])] * len(i[1])))
                    summary .append((i[0], [('fail', i[2].exc, i[2].msg)]))
                    errors  .append(i[2])
                    failed += len(i[1])
                    synfailed = True
                else:
                    overview.append((i[0], [('skip',)] * len(i[1])))
                    summary .append((i[0], [('skip', i[2].msg, i[2].msg)]))
            else:
                overview.append((i[0], []))
                summary .append((i[0], []))
                for key, value in pb(i[1].items(), label=i[0]):
                    res = RTResult()
                    res.register(
                        value.call(key, {}, {}, {})
                    )

                    if isinstance(res.testreturn, periscope.PeriSkip):
                        overview[-1][1].append(('skip',))
                        summary [-1][1].append(('skip', res.testreturn.msg))
                    elif res.error:
                        overview[-1][1].append(('fail', res.error))
                        summary [-1][1].append(('fail', res.error.exc, res.error.msg))
                        errors         .append(res.error)
                        failed += 1
                    else:
                        overview[-1][1].append(('pass',))
                        passed += 1



    size = get_terminal_size()
    text = ' Overview '
    left = '═' * (int(size[0] / 2) - int(len(text) / 2))
    right = '═' * (size[0] - len(text) - len(left))
    pprint(f'\n{escape(left)}<bold>{escape(text)}</bold>{escape(right)}\n', style=style, color_depth=ColorDepth.TRUE_COLOR)

    maxlen = 0
    for i in overview:
        if len(i[0]) > maxlen:
            maxlen = len(i[0])

    for i in overview:
        iover = ''
        for j in i[1]:
            if j[0] == 'pass':
                iover += '<ansigreen>•</ansigreen>'
            elif j[0] == 'skip':
                iover += '<ansiyellow>⏵</ansiyellow>'
            else:
                iover += '<ansired><bold>×</bold></ansired>'
        pprint(f' <ansiblue><bold>{escape(i[0].ljust(maxlen))}</bold></ansiblue>: {iover}', style=style, color_depth=ColorDepth.TRUE_COLOR)



    if failed >= 1 or synfailed:
        size = get_terminal_size()
        text = ' Errors '
        left = '═' * (int(size[0] / 2) - int(len(text) / 2))
        right = '═' * (size[0] - len(text) - len(left))
        pprint(f'\n{escape(left)}<bold>{escape(text)}</bold>{escape(right)}\n', style=style, color_depth=ColorDepth.TRUE_COLOR)

        for i in range(len(errors)):
            err = errors[i].asstring().split('\n')
            err = err[1:-2]
            err = '\n'.join(err)
            print(err)

            if i < len(errors) - 1:
                pprint(f'{escape("─" * get_terminal_size()[0])}', color_depth=ColorDepth.TRUE_COLOR)



    if max([len(i[1]) for i in summary]) >= 1:
        size = get_terminal_size()
        text = ' Summary '
        left = '═' * (int(size[0] / 2) - int(len(text) / 2))
        right = '═' * (size[0] - len(text) - len(left))
        pprint(f'\n{escape(left)}<bold>{escape(text)}</bold>{escape(right)}\n', style=style, color_depth=ColorDepth.TRUE_COLOR)

        maxlen = 0
        for i in summary:
            for j in i[1]:
                if j[0] == 'fail':
                    if len(j[1]) >= 1:
                        maxlen = len(j[1]) + 1

        for i in summary:
            if len(i[1]) >= 1:
                pprint(f' <ansiblue><bold>{escape(i[0])}</bold></ansiblue>:')
                for j in i[1]:
                    if j[0] == 'skip':
                        pprint(f'   <ansiyellow>Skipped</ansiyellow>: {escape(" " * maxlen)}   <ansiyellow><bold>{escape(j[1])}</bold></ansiyellow>')
                    elif j[0] == 'fail':
                        pprint(f'    <ansired>Failed</ansired>: <ansired>{escape(j[1].ljust(maxlen))}</ansired> - <ansired><bold>{escape(j[2])}</bold></ansired>')



    endtime = datetime.now()
    timetaken = endtime - starttime
    timetaken = round(timetaken.total_seconds(), 2)
    timetaken = format(timetaken, '.2f') + 's'


    size = get_terminal_size()
    passedtext = ''
    if passed >= 1 or failed == 0:
        passedtext = f'{passed} passed'
    combiner = ''
    if passed >= 1 and (failed >= 1 or synfailed):
        combiner = ', '
    failedtext = ''
    if failed >= 1 or synfailed:
        failedtext = f'{failed} failed'
    text = f' {passedtext}{combiner}{failedtext} in {timetaken} '
    left = '═' * (int(size[0] / 2) - int(len(text) / 2))
    right = '═' * (size[0] - len(text) - len(left))
    if passed >= 1 and failed == 0 and not synfailed:
        passedtext = f'<bold>{passedtext}</bold>'

    text = f' <ansigreen>{passedtext}</ansigreen>{combiner}<ansired><bold>{failedtext}</bold></ansired> '
    linecolour = 'green'
    if failed >= 1 or synfailed:
        linecolour = 'red'
    pprint(f'\n<ansi{escape(linecolour)}>{left}</ansi{linecolour}>{text}<ansi{linecolour}>in {timetaken} {right}</ansi{linecolour}>\n', style=style, color_depth=ColorDepth.TRUE_COLOR)

    return(bool(failed))
