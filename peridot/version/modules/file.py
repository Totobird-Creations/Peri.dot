import io

import perimod
from perimod import success, failure

pyopen = open

modetypes = {
    'r'  : 'read-only',
    'r+' : 'read-write',
    'w'  : 'write-only',
    'w+' : 'write-read',
    'rb' : 'read-only (binary)',
    'rb+': 'read-write (binary)',
    'wb+': 'write-read (binary)',
    'a'  : 'append-only',
    'ab' : 'append (binary)',
    'a+' : 'append-read',
    'ab+': 'append-read (binary)',
    'x'  : 'create-only'
}

class FileType(perimod.Type):
    def __init__(self, name, value=None):
        if not isinstance(value, io.IOBase):
            raise perimod.InternalPeridotError(f'Non TextIOWrapper value receievd ({type(value).__name__})')
        super().__init__(value, type_='FileType')
        self.filename = name

    def tostr(self):
        return((
            perimod.StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def copy(self):
        copy = FileType(self.filename, self.value)
        copy.id = self.id
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)

        return(copy)

    def attribute(self, attribute):
        if attribute.value == 'read':
            f = perimod.BuiltInFunctionType(f'{perimod._file}.read')
            f.setcontext(self.context)
            f.setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'write':
            f = perimod.BuiltInFunctionType(f'{perimod._file}.write')
            f.setcontext(self.context)
            f.setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'close':
            f = perimod.BuiltInFunctionType(f'{perimod._file}.close')
            f.setcontext(self.context)
            f.setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        else:
            return((None, perimod.Exc.TypeError(f'\'{self.name}\' has no attribute \'{attribute.value}\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def __repr__(self):
        return(f'<File \'{self.filename}\'>')



@perimod.module
def main(context, pos):
    # Functions
    def open(self, exec_context, args, opts):
        file = args['file']
        mode = opts['mode']
        try:
            f =  pyopen(file.value, mode.value)
            f = FileType(file.value, f)
            return(success(
                f
            ))
        except FileNotFoundError:
            return(failure(
                perimod.Exc.FileAccessError(
                    f'File \'{file.value}\' could not be found',
                    file.start, file.end,
                    context,
                    file.originstart, file.originend, file.origindisplay
                )
            ))
        except IsADirectoryError:
            return(failure(
                perimod.Exc.FileAccessError(
                    f'File \'{file.value}\' is a directory',
                    file.start, file.end,
                    context,
                    file.originstart, file.originend, file.origindisplay
                )
            ))
        except PermissionError:
            return(failure(
                perimod.Exc.FileAccessError(
                    f'File \'{file.value}\' could not be accessed: Restricted access',
                    file.start, file.end,
                    context,
                    file.originstart, file.originend, file.origindisplay
                )
            ))
        except ValueError:
            return(failure(
                perimod.Exc.ValueError(
                    f'Invalid mode: \'{mode.value}\'',
                    mode.start, mode.end,
                    context,
                    mode.originstart, mode.originend, mode.origindisplay
                )
            ))
    open.argnames = {'file': perimod.StringType}
    open.optnames = {'mode': perimod.StringType('r')}
    perimod.assign('open', open)



    # Type Attributes
    def read(self, exec_context, args, opts):
        if self.editvalue.value.closed:
            return(failure(
                perimod.Exc.ValueError(
                    f'Can not read from a closed file object',
                    self.start, self.end,
                    exec_context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

        try:
            string = self.editvalue.value.read()
        except io.UnsupportedOperation:
            return(failure(
                perimod.Exc.ValueError(
                    f'Can not read from a {modetypes[self.editvalue.value.mode]} file object',
                    self.start, self.end,
                    exec_context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

        return(success(
            perimod.StringType(string)
        ))
    perimod.typeattr(read)


    def write(self, exec_context, args, opts):
        if self.editvalue.value.closed:
            return(failure(
                perimod.Exc.ValueError(
                    f'Can not write to a closed file object',
                    self.start, self.end,
                    exec_context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

        try:
            self.editvalue.value.write(
                args['text'].value
            )
        except io.UnsupportedOperation:
            return(failure(
                perimod.Exc.ValueError(
                    f'Can not write to a {modetypes[self.editvalue.value.mode]} file object',
                    self.start, self.end,
                    exec_context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

        return(success(
            perimod.NullType()
        ))
    write.argnames = {'text': perimod.StringType}
    perimod.typeattr(write)


    def close(self, exec_context, args, opts):
        if self.editvalue.value.closed:
            return(failure(
                perimod.Exc.ValueError(
                    f'Can not close a closed file object',
                    self.start, self.end,
                    exec_context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

        self.editvalue.value.close()

        return(success(
            perimod.NullType()
        ))
    perimod.typeattr(close)
