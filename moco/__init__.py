import types
import connections
from errors import (Error, Warning, InterfaceError, DatabaseError, DataError,
                    OperationalError, IntegrityError, InternalError,
                    ProgrammingError, NotSupportedError)
from times import (Date, Time, Timestamp, DateFromTicks, TimeFromTicks,
                   TimestampFromTicks)

threadsafety = 1
apilevel = '2.0'
paramstyle = 'format'


class DBAPISet(frozenset):

    def __ne__(self, other):
        if isinstance(other, set):
            return super(DBAPISet, self).__ne__(self, other)
        else:
            return other not in self

    def __eq__(self, other):
        if isinstance(other, frozenset):
            return frozenset.__eq__(self, other)
        else:
            return other in self

    def __hash__(self):
        return frozenset.__hash__(self)


STRING = DBAPISet([types.ENUM, types.STRING,
                     types.VAR_STRING])
BINARY = DBAPISet([types.BLOB, types.LONG_BLOB,
                     types.MEDIUM_BLOB, types.TINY_BLOB])
NUMBER = DBAPISet([types.DECIMAL, types.DOUBLE, types.FLOAT,
                     types.INT24, types.LONG, types.LONGLONG,
                     types.TINY, types.YEAR])
DATE = DBAPISet([types.DATE, types.NEWDATE])
TIME = DBAPISet([types.TIME])
TIMESTAMP = DBAPISet([types.TIMESTAMP, types.DATETIME])
DATETIME = TIMESTAMP
ROWID = DBAPISet()


def Binary(x):
    return str(x)


def connect(*args, **kwargs):
    return connections.Connection(*args, **kwargs)
Connection = Connect = connect
