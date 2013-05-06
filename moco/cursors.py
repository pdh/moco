from errors import ProgrammingError
from sys import exc_info
from weakref import proxy

class Cursor(object):

    def __init__(self, connection):
        self.connection = proxy(connection)
        self.description = None
        self.rownumber = 0
        self.rowcount = -1
        self.arraysize = 1
        self._executed = None
        self.messages = []
        self.errorhandler = connection.errorhandler
        self._rows = None

    def __del__(self):
        self.close()

    def close(self):
        self.connection = None

    def _check_executed(self):
        if not self._executed:
            self.errorhandler(self, ProgrammingError, 'execute() first')
        if self._rows is None:
            self.errorhandler(self, ProgrammingError, 'no-result query')

    def setinputsizes(self, *args):
        pass

    def setoutputsize(self, *args):
        pass

    def nexset(self):
        pass

    def _get_results(self):
        self.rownumber = 0
        self.rowcount = 0
        self._rows = None
        self.description = None
        if isinstance(self._result, tuple):
            self.rowcount = self._result[0] if self._result[0] > 0 else -1
        else:
            self._rows = self._result.rows
            self.rowcount = len(self._rows)
            self.description = (list(self._result.fields[0]) + [None] * 5,)

    def execute(self, query, args=None):
        args = tuple(args) if args else ()
        try:
            self._result = self.connection._query(query, args)
        except:
            exc, value, tb = exc_info()
            self.errorhandler(self, exc, value)
        self._get_results()
        self._executed = query
        return self.rowcount

    def executemany(self, query, args):
        if not args:
            return
        self.rowcount = sum([self.execute(query, arg) for arg in args])
        return self.rowcount

    def fetchone(self):
        self._check_executed()
        if self._rows is None or self.rownumber >= len(self._rows):
            return None
        result = self._rows[self.rownumber]
        self.rownumber += 1
        return result

    def fetchmany(self, size=None):
        self._check_executed()
        end = self.rownumber + (size or self.arraysize)
        result = self._rows[self.rownumber:end]
        if self._rows is None:
            return None
        self.rownumber = min(end, len(self._rows))
        return result

    def fetchall(self):
        self._check_executed()
        if self._rows is None:
            return None
        if self.rownumber:
            result = self._rows[self.rownumber:]
        else:
            result = self._rows
        self.rownumber = len(self._rows)
        return result

    def scroll(self, value, mode='relative'):
        pass

    def __iter__(self):
        self._check_executed()
        result = self.rownumber and self._rows[self.rownumber:] or self._rows
        return iter(result)
