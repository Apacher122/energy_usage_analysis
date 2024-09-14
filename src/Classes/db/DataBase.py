import sqlite3

class Database:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self.table = kwargs.get('table')

    @property
    def filename(self): return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename
        self._db = sqlite3.connect(filename)
        self._db.row_factory = sqlite3.Row

    @filename.deleter
    def filename(self): return self.close()

    @property
    def table(self): return self._table

    @table.setter
    def table(self, table): self._table = table

    @table.deleter
    def table(self): self._table = ''

    def close(self):
        self._db.close()
        del self._filename
