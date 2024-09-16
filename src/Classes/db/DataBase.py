""" This will eventually be used :( """
import sqlite3

class Database:
    """ Da DB """
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self.table = kwargs.get('table')

    @property
    def filename(self):
        """ Da filename """
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename
        self._db = sqlite3.connect(filename)
        self._db.row_factory = sqlite3.Row

    @filename.deleter
    def filename(self):
        """ da deleter """
        return self.close()

    @property
    def table(self):
        """ da table """
        return self._table

    @table.setter
    def table(self, table):
        """ setting the table is good manners """
        self._table = table

    @table.deleter
    def table(self):
        """ Oh no... our table... is broken """
        self._table = ''

    def close(self):
        """ goodbye """
        self._db.close()
        del self._filename
