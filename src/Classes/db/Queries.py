from Classes.db import DataBase
import sqlite3
from datetime import datetime

dt_format = "%d/%m/%Y %H:%M:%S"

class UsageQueries:
    def __init__(self, **kwargs):
        self._con = sqlite3.connect(kwargs.get('filename'))
        self.table = kwargs.get('table', 'device')
        self._cur = self._con.cursor()
        try:
            self._cur.execute("PRAGMA journal_mode=wal")
        except sqlite3.Error as err:
            print(err)

    def insert(self, data):
        db = self._cur
        try:
            db.executemany("INSERT INTO {table_name} VALUES (:date_time, :device, :wattage)".format(table_name=self._table), data)
            self._con.commit()
        except sqlite3.Error as err:
            print(err)

    # def get_hourly_data(self):
    #     try:
    #         db.execute("""
    #                    SELECT date_time, device, wattage
    #                    FROM air_conditioner 
    #                    WHERE strftime('%T', date_time)  < '05:59:59';
    #                    """)

    @property
    def table(self): return self._table

    @table.setter
    def table(self, table):
        tn = ""
        match table.strip():
            case 'Air conditioner':
                self._table = 'air_conditioner'
            case 'air purifier':
                self._table = 'air_purifier'
            case 'Central Plug Top':
                self._table = 'central_plug_top'
            case 'Power Strip (peripherals)':
                self._table = 'power_strip'
            case 'Monitors':
                self._table = 'monitors'
            case 'Personal PC':
                self._table = 'personal_pc'
            case "Jupi’s light":
                self._table = 'jupis_light'
            case _:
                self._table = "ERR"

        sql = f"CREATE TABLE IF NOT EXISTS {self._table} (date_time DATETIME, device, wattage)"
        self._con.execute(sql)



    