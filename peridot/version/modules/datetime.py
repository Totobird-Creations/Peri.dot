import os
import sys
import datetime as dt

import perimod
from perimod import success, failure

class DatetimeType(perimod.Type):
    def __init__(self, value=None):
        if not isinstance(value, dt.datetime):
            raise perimod.InternalPeridotError(f'Non datetime value receievd ({type(value).__name__})')
        super().__init__(value, type_='DatetimeType')

    def tostr(self):
        return((
            perimod.StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def attribute(self, attribute):
        if attribute.value == 'strftime':
            f = perimod.BuiltInFunctionType(f'{perimod._file}_strftime')
            f.setcontext(self.context)
            f.setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        else:
            return((None, perimod.Exc.TypeError(f'\'{self.name}\' has no attribute \'{attribute.value}\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def copy(self):
        copy = DatetimeType(self.value)
        copy.id = self.id
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)

        return(copy)

    def __repr__(self):
        year        = str(self.value.year)       .rjust(4, '0')
        month       = str(self.value.month)      .rjust(2, '0')
        date        = str(self.value.day)        .rjust(2, '0')
        hour        = str(self.value.hour)       .rjust(2, '0')
        minute      = str(self.value.minute)     .rjust(2, '0')
        second      = str(self.value.second)     .rjust(2, '0')
        microsecond = str(self.value.microsecond).rjust(6, '0')
        return((f'<Datetime {year}-{month}-{date} {hour}:{minute}:{second}.{microsecond}>'))



@perimod.module
def main(context, pos):
    # Types
    def datetime(self, exec_context, args, opts):
        year        = exec_context.symbols.access('y')
        try:
            dt.datetime(year=year.value, month=1, day=1)
        except ValueError:
            return(failure(perimod.Exc.Exc_ValueError(
                f'Year must be in range: 1..9999',
                year.start, year.end,
                exec_context,
                year.originstart, year.originend, year.origindisplay
            )))

        month       = exec_context.symbols.access('m')
        try:
            dt.datetime(year=year.value, month=month.value, day=1)
        except ValueError:
            return(failure(perimod.Exc.Exc_ValueError(
                f'Month must be in range: 1..12',
                month.start, month.end,
                exec_context,
                month.originstart, month.originend, month.origindisplay
            )))

        date         = exec_context.symbols.access('d')
        try:
            dt.datetime(year=year.value, month=month.value, day=date.value)
        except ValueError:
            return(failure(perimod.Exc.Exc_ValueError(
                f'Date must be in range: 1..(28~31)',
                date.start, date.end,
                exec_context,
                date.originstart, date.originend, date.origindisplay
            )))

        hour        = exec_context.symbols.access('H')
        try:
            dt.datetime(year=year.value, month=month.value, day=date.value, hour=hour.value)
        except ValueError:
            return(failure(perimod.Exc.Exc_ValueError(
                f'Hour must be in range: 0..23',
                hour.start, hour.end,
                exec_context,
                hour.originstart, hour.originend, hour.origindisplay
            )))

        minute      = exec_context.symbols.access('M')
        try:
            dt.datetime(year=year.value, month=month.value, day=date.value, hour=hour.value, minute=minute.value)
        except ValueError:
            return(failure(perimod.Exc.Exc_ValueError(
                f'Minute must be in range: 0..59',
                minute.start, minute.end,
                exec_context,
                minute.originstart, minute.originend, minute.origindisplay
            )))

        second      = exec_context.symbols.access('S')
        try:
            dt.datetime(year=year.value, month=month.value, day=date.value, hour=hour.value, minute=minute.value, second=second.value)
        except ValueError:
            return(failure(perimod.Exc.Exc_ValueError(
                f'Second must be in range: 0..59',
                second.start, second.end,
                exec_context,
                second.originstart, second.originend, second.origindisplay
            )))

        microsecond = exec_context.symbols.access('f')
        try:
            dt.datetime(year=year.value, month=month.value, day=date.value, hour=hour.value, minute=minute.value, second=second.value, microsecond=microsecond.value)
        except ValueError:
            return(failure(perimod.Exc.Exc_ValueError(
                f'Microsecond must be in range: 0..999999',
                microsecond.start, microsecond.end,
                exec_context,
                microsecond.originstart, microsecond.originend, microsecond.origindisplay
            )))

        return(success(
            DatetimeType(
                dt.datetime(
                    year.value, month.value, date.value,
                    hour.value, minute.value, second.value,
                    microsecond.value
                )
            )
        ))
    datetime.optnames = {
        'y': perimod.IntType(1), # Year
        'm': perimod.IntType(1), # Month
        'd': perimod.IntType(1), # Date
        'H': perimod.IntType(0), # Hour
        'M': perimod.IntType(0), # Minute
        'S': perimod.IntType(0), # Second
        'f': perimod.IntType(0)  # Microsecond
    }
    perimod.assign('datetime', datetime)



    # Type Attributes
    def strftime(self, exec_context, args, opts):
        format = args['format']

        string = self.editvalue.value.strftime(format.value)

        return(success(
            perimod.StringType(string)
        ))
    strftime.argnames = {
        'format': perimod.StringType
    }
    perimod.typeattr(strftime)



    # Functions
    def now(self, exec_context):
        return(success(
            DatetimeType(
                dt.datetime.now()
            )
        ))
    perimod.assign('now', now)
