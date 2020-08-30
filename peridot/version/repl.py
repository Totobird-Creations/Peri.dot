##########################################
# DEPENDENCIES                           #
##########################################

from os import get_terminal_size, getcwd
from time import strftime
from pathlib import Path

from   pygments.token                      import Token

from   prompt_toolkit.formatted_text       import PygmentsTokens        as PygTokens
from   prompt_toolkit.lexers               import PygmentsLexer
from   prompt_toolkit                      import PromptSession
from   prompt_toolkit                      import print_formatted_text
from   prompt_toolkit.styles               import Style
from   prompt_toolkit.completion           import Completer, Completion
from   prompt_toolkit.history              import FileHistory
from   prompt_toolkit.key_binding          import KeyBindings
from   prompt_toolkit.application.current  import get_app
from   prompt_toolkit.enums                import EditingMode
from   prompt_toolkit.key_binding.vi_state import InputMode
from   prompt_toolkit.shortcuts            import button_dialog
from   prompt_toolkit.validation           import Validator, ValidationError
from   prompt_toolkit.application          import Application
from   prompt_toolkit.output               import ColorDepth
from   prompt_toolkit                      import print_formatted_text as printf
from   prompt_toolkit.formatted_text       import FormattedText
import xdgappdirs

def _replinit(version, default, context, runu, lexer, parser, interpreter):
    global VERSION
    VERSION = version
    global defaultvariables
    defaultvariables = default.defaultvariables
    global SymbolTable
    SymbolTable      = context.SymbolTable
    global run
    run              = runu.run
    global Lexer
    Lexer = lexer.Lexer
    global Parser
    Parser = parser.Parser
    global Interpreter
    Interpreter = interpreter.Interpreter


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


class ExitCalledException(BaseException): pass

class Completer(Completer):
    def __init__(self,
        style, keyword_constant, keyword_declaration, keyword_namespace, keyword_reserved, keyword_types
    ):
        self.style = style

        self.keyword_constant    = sorted(keyword_constant)
        self.keyword_declaration = sorted(keyword_declaration)
        self.keyword_namespace   = sorted(keyword_namespace)
        self.keyword_reserved    = sorted(keyword_reserved)
        self.keyword_types       = sorted(keyword_types)
        self.words = sorted(
            self.keyword_constant + self.keyword_declaration + self.keyword_namespace + self.keyword_reserved + self.keyword_types
        )
        self.ignore_case = False
        self.meta_dict = {}
        self.WORD = False
        self.sentence = False
        self.match_middle = False
        self.pattern = None

    def createapp(self, input, output):
        return(
            Application
        )

    def get_completions(self, document, complete_event):
        words = self.words

        if self.sentence:
            word_before_cursor = document.text_before_cursor
        else:
            word_before_cursor = document.get_word_before_cursor(
                WORD=self.WORD, pattern = self.pattern
            )

        if self.ignore_case:
            word_before_cursor = word_before_cursor.lower()

        def word_matches(word):
            if self.ignore_case:
                word = word.lower()

            if self.match_middle:
                return(word_before_cursor in word)
            else:
                return(word.startswith(word_before_cursor))

        for i in words:
            if word_matches(i):
                display_meta = self.meta_dict.get(i, '')
                if i in self.keyword_constant:
                    cstyle = self.style['pygments.keyword.constant']
                elif i in self.keyword_declaration:
                    cstyle = self.style['pygments.keyword.declaration']
                elif i in self.keyword_namespace:
                    cstyle = self.style['pygments.keyword.namespace']
                elif i in self.keyword_reserved:
                    cstyle = self.style['pygments.keyword.reserved']
                elif i in self.keyword_types:
                    cstyle = self.style['pygments.keyword.types']
                else:
                    cstyle = '#222222'

                yield(Completion(i, -len(word_before_cursor), display_meta=display_meta, style=cstyle))


class PromptToolkitRepl():
    style = {
        'title'  : '#00ff00 bold',
        'linksub': '#007700',
        'link'   : '#00dd00 italic',

        'promptcwd'                   : 'bg:#295183 #d9dcd6',
        'prompttimestart'             : 'bg:#9D8000 #295183',
        'prompttime'                  : 'bg:#9D8000 #14191b',
        'promptsuccessstart'          : 'bg:#00c000 #9D8000',
        'promptsuccess'               : 'bg:#00c000 #14191b',
        'promptsuccessend'            : '#00c000',
        'promptfailedstart'           : 'bg:#c00000 #9D8000',
        'promptfailed'                : 'bg:#c00000 #14191b',
        'promptfailedend'             : '#c00000',
        'prompt'                      : '#d9dcd6',

        'completion'                  : '#c00000',

        'toolbar'                     : '#ffffff',
        'toolbar.keybind'             : 'bg:#ffffff #aa5555',
        'toolbar.state'               : 'bg:#ffffff #777722',
        'toolbar.error'               : 'bg:#d9dcd6 #c00000',

        'pygments.keyword.constant'   : '#569cd6',
        'pygments.keyword.declaration': '#c586c0',
        'pygments.keyword.namespace'  : '#c586c0',
        'pygments.keyword.reserved'   : '#c586c0',
        'pygments.keyword.types'      : '#4ec9b0',

        'dialog'                      : 'bg:#0a0a0a',
        'dialog.body'                 : 'bg:#3a3a3a',
        'dialog frame'                : '#ff0000',
        'dialog frame.label'          : '#ff0000',
        'dialog shadow'               : 'bg:#1a1a1a'
    }
    theme = Style.from_dict(style)

    KEYWORD_CONSTANT    = ['True', 'False', 'Null']
    KEYWORD_DECLARATION = ['var', 'func', 'lambda', 'as', 'in']
    KEYWORD_NAMESPACE   = ['include']
    KEYWORD_RESERVED    = ['and', 'or', 'not', 'return', 'if', 'elif', 'else', 'switch', 'when', 'for', 'while', 'continue', 'break', 'handler']
    KEYWORD_TYPES       = ['id', 'str', 'int', 'float', 'bool', 'array', 'tuple']

    completer = Completer(
        style, KEYWORD_CONSTANT, KEYWORD_DECLARATION, KEYWORD_NAMESPACE, KEYWORD_RESERVED, KEYWORD_TYPES
    )
    session = PromptSession(
        history=FileHistory(xdgappdirs.user_data_dir('Peridot', 'TotobirdCreations', as_path=True) / '.replhistory')
    )



    def validate(self, text):
        lexer = Lexer('<repl>', text)
        tokens, error = lexer.maketokens()

        if error:
            return(f'{error.exc}: {error.msg} ({error.start.line + 1}:{error.start.column + 1})')

        if len(tokens) - 2:
            parser = Parser(tokens)
            ast = parser.parse()

            if ast.error:
                error = ast.error
                return(f'{error.exc}: {error.msg} ({error.start.line + 1}:{error.start.column + 1})')

    def execute(self, text):
        result, exec_context, error = run('<repl>', text, self.symbols)
        if error:
            print(error.asstring())
            self.prevstatus = 1

        else:
            print('\n'.join(str(i) for i in result))


    def genprompt(self):
        mode   = 'failed' if self.prevstatus else 'success'
        status = str(self.prevstatus) if self.prevstatus else '✓'

        return([
            ('class:prompt', '' if self.first else '\n'),
            ('class:prompt', '❯❯❯ ')
        ])

        #return([
            #('class:prompt', '' if self.first else '\n'),
            #('class:promptcwd', ' ' + str(self.cwd) + ' '),
            #('class:prompttimestart', ' '),
            #('class:prompttime', self.time + ' '),
            #(f'class:prompt{mode}start', ' '),
            #(f'class:prompt{mode}', status + ' '),
            #(f'class:prompt{mode}end', ''),
            #('class:prompt', '\n❯ ')
        #])

    def prompt_continuation(self, width, line_number, is_soft_wrap):
        return([
            ('class:prompt', '  ❯ ')
        ])


    vistates = {
        'vi-insert'         : 'Insert',
        'vi-insert-multiple': 'Insert Multiple',
        'vi-navigation'     : 'Navigation',
        'vi-replace'        : 'Replace',
        'vi-replace-single' : 'Replace Single'
    }
    def toolbar(self):
        if get_app().editing_mode == EditingMode.VI:
            mode = 'Vi'
            state = f'({self.vistates[get_app().vi_state.input_mode]})'
        else:
            mode = 'Emacs'
            state = ''
        return([
            ('class:toolbar.keybind', '[F4]'),
            ('', ' '),
            ('class:toolbar', mode),
            ('', ' '),
            ('class:toolbar.state', state),
            ('', ' '),
            ('class:toolbar.error', self.error if self.error else '')
        ])


    def main(self):
        self.first = True
        self.prevstatus = 0
        self.error = None
        self.symbols = defaultvariables(SymbolTable())
        while True:
            self.time = strftime('🕗 %H:%M:%S')
            self.cwd  = Path(getcwd())
            try:
                script = self.session.prompt(
                    self.genprompt(),
                    prompt_continuation=self.prompt_continuation,
                    style=self.theme,
                    completer=self.completer,
                    complete_while_typing=True,
                    bottom_toolbar=self.toolbar,
                    vi_mode=False,
                    key_bindings=self.bindings,
                    wrap_lines=False
                )
                if not script:
                    script = self.result

                self.execute(script)
            except KeyboardInterrupt: continue
            self.first = False

    def __init__(self):
        printf(FormattedText([
            ('class:title'  , 'Peridot 1.1.0'),
            (''             , '\n'),
            ('class:linksub', ' Homepage: '),
            ('class:link'   , 'https://toto-bird.github.io/Peri.dot-lang/'),
            (''             , '\n'),
            ('class:linksub', ' Documentation: '),
            ('class:link'   , 'https://toto-bird.github.io/Peri.dot-lang/docs'),
            (''             , '\n')
        ]), style=self.theme)

        
        self.bindings = KeyBindings()

        @self.bindings.add('f4')
        def _(event):
            app = event.app

            if app.editing_mode == EditingMode.VI:
                app.editing_mode = EditingMode.EMACS
            else:
                app.editing_mode = EditingMode.VI
                app.vi_state.input_mode = InputMode('vi-navigation')

        @self.bindings.add('c-d')
        def _(event):
            text = event.current_buffer.text
            if len(text) == 0:
                event.app.exit(exception=ExitCalledException)

        @self.bindings.add('enter')
        def _(event):
            text = event.current_buffer.text
            lines = text.split('\n')
            position = [0, 0]
            for i in range(event.current_buffer.cursor_position):
                if position[0] >= len(lines[position[1]]):
                    position = [0, position[1] + 1]
                else:
                    position[0] += 1
            if position[0] == 0 and len(lines[position[1]]) == 0 and len(lines) - 1 == position[1]:
                if len(text.replace('\n', '').replace(' ', '').replace('\t', '')) >= 1:
                    self.prevstatus = 0
                    check = self.validate(text)
                    self.error = check
                    if not check:
                        self.result = text
                        event.app.exit()
            else:
                event.current_buffer.insert_text('\n')

        try:
            self.main()
        except ExitCalledException: pass
