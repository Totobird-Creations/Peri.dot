def _runinit(lexer, parser, context, interpreter):
    global Lexer, Parser, Context, Interpreter
    Lexer = lexer.Lexer
    Parser = parser.Parser
    Context = context.Context
    Interpreter = interpreter.Interpreter

def run(filename, script, symbols):
    lexer = Lexer(filename, script)
    tokens, error = lexer.maketokens()

    if error:
        return((None, None, error))

    if len(tokens) - 2:
        parser = Parser(tokens)
        ast = parser.parse()

        if ast.error:
            return((None, None, ast.error))

        context = Context('<file>', symbols=symbols)

        nodes = []
        for i in ast.node:
            interpreter = Interpreter()
            result = interpreter.visit(i, context)

            if result.error:
                return((None, None, result.error))

            nodes.append(result.value)

        return((nodes, context, None))

    return(([], None, None))
