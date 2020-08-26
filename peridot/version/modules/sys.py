import os
import sys

from ..        import perimod
from ..perimod import Types
from ..perimod import success, failure

@perimod.module
def main():
    # Setup
    context = perimod.Context
    symbols = perimod.Symbols
    pos     = perimod.Position



    # Functions
    def terminalsize(self, exec_context):
        size = os.get_terminal_size()
        size = (Types.IntType(size[0]), Types.IntType(size[1]))

        return(success(
            Types.TupleType(size)
        ))

    perimod.BuiltInFuncs['terminalsize'] = terminalsize
    terminalsize = Types.BuiltInFunctionType('terminalsize').setcontext(context).setpos(pos.start, pos.end)
    symbols.assign('terminalsize', terminalsize)



    # Variables
    symbols.assign(
        'args',
        Types.ArrayType(
            [Types.StringType(i) for i in sys.argv]
        )
    )
