from .context     import Context, SymbolTable
from .interpreter import Interpreter
from .lexer       import Lexer
from .parser      import Parser

def run(filename, script, symbols):
    lexer = Lexer(filename, script)
    tokens, error = lexer.maketokens()

    if error:
        return((None, error))

    if len(tokens) - 2:
        parser = Parser(tokens)
        ast = parser.parse()

        if ast.error:
            return((None, ast.error))

        context = Context('<file>', symbols=symbols)

        nodes = []
        for i in ast.node:
            interpreter = Interpreter()
            result = interpreter.visit(i, context)

            if result.error:
                return((None, result.error))

            nodes.append(result.value)

        return((nodes, None))

    return(([], None))