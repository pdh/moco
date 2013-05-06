import sys
import umysql
from errors import (Error, Warning, InterfaceError, DatabaseError, DataError,
                    OperationalError, IntegrityError, InternalError,
                    ProgrammingError, NotSupportedError)
from cursors import Cursor


DEFAULT_CHARSET = 'latin1'


def defaulterrorhandler(connection, cursor, error_class, error_value):
    if not issubclass(error_class, Error):
        raise Error(error_class, error_value)
    else:
        raise error_class, error_value


class Connection(object):

    errorhandler = defaulterrorhandler

    def __init__(self, host='localhost', port=3306, user=None, passwd='',
                 db=None, charset=None, cursorclass=Cursor, use_unicode=None,
                 connect_timeout=None, autocommit=False):
        self.host = host
        self.port = port
        self.user = user
        self.password = passwd
        self.db = db
        self.charset = charset or DEFAULT_CHARSET
        self.cursorclass = cursorclass
        self.connect_timeout = connect_timeout
        self.autocommit = autocommit
        self._connect()

    def _connect(self):
        self.connection = umysql.Connection()
        self.connection.connect(self.host, self.port, self.user,
                                self.password, self.db, self.autocommit,
                                self.charset)

    def close(self):
        if self.connection is None:
            raise Error('Already closed.')
        self.connection = None

    def cursor(self):
        return self.cursorclass(self)

    def _query(self, query, args):
        return self.connection.query(query, args)

    def commit(self):
        try:
            self._query('COMMIT', ())
        except:
            exc, value, tb = sys.exc_info()
            self.errorhandler(None, exc, value)

    def rollback(self):
        try:
            self._query('ROLLBACK', ())
        except:
            exc, value, tb = sys.exc_info()
            self.errorhandler(None, exc, value)

    Warning = Warning
    Error = Error
    InterfaceError = InterfaceError
    DatabaseError = DatabaseError
    DataError = DataError
    OperationalError = OperationalError
    IntegrityError = IntegrityError
    InternalError = InternalError
    ProgrammingError = ProgrammingError
    NotSupportedError = NotSupportedError
