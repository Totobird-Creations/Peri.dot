import os
import sys

import perimod
from perimod import success, failure

@perimod.module
def main(context, pos):
    # Functions
    def terminalsize(self, exec_context, args, opts):
        size = os.get_terminal_size()
        size = (size[0], size[1])

        return(success(
            size
        ))
    perimod.assign('terminalsize', terminalsize)



    # Variables
    perimod.assign(
        'args',
        sys.argv
    )
