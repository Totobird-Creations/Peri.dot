import perimod
from perimod import success, failure

class PeriSkip(perimod.Type):
    def __init__(self, msg):
        super().__init__(type_='PeriSkip')
        self.msg = msg

    def tostr(self):
        return((
            perimod.StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def copy(self):
        copy = PeriSkip(self.msg)
        copy.id = self.id
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)

        return(copy)

    def __repr__(self):
        return(f'<PeriscopeStatus: Skip>')



@perimod.module
def main(context, pos):
    # Types
    def skip(self, exec_context, args, opts):
        return(success(
            PeriSkip(args['msg'].value)
                .setpos(pos.start, pos.end)
                .setcontext(context)
        ))
    skip.argnames = {
        'msg': perimod.StringType
    }
    perimod.assign('skip', skip)
