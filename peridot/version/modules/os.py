import os

from ..context import SymbolTable
from ..default import defaultvariables
from ..types   import IntType, TupleType, BuiltInFunctionType, NamespaceType, RTResult

def main(context, start, end):
    # Built-In Functions
    def terminalsize(exec_context):
        res = RTResult()
        size = os.get_terminal_size()
        size = (IntType(size[0]), IntType(size[1]))
        return(
            res.success(
                TupleType(size)
            )
        )
    terminalsize.argnames = {}
    terminalsize.optnames = {}

    BuiltInFunctionType.modules['exec_terminalsize'] = terminalsize
    terminalsize = BuiltInFunctionType('terminalsize')
    terminalsize.setcontext(context).setpos(start, end)


    # Module Object
    symbols = defaultvariables(SymbolTable(context.symbols))
    symbols.assign('terminalsize', terminalsize)

    namespace = NamespaceType(symbols)
    return(namespace)
