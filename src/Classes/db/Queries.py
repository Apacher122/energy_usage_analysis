""" Query the database for good vibes """
import sqlite3

DT_FORMAT = "%d/%m/%Y %H:%M:%S"

class HAQueries:
    """ Queries for Home Assistant data """
    def __init__(self, **kwargs):
        self._con = sqlite3.connect(kwargs.get('filename'))
        self.table = kwargs.get('table', 'device')
        self._cur = self._con.cursor()
        try:
            self._cur.execute("PRAGMA journal_mode=wal")
        except sqlite3.Error as err:
            print(err)

    def insert(self, data):
        """ insert into db """
        db = self._cur
        try:
            db.executemany("""
                INSERT OR IGNORE INTO usage_data VALUES (
                    :record_date,
                    :entity_id,
                    :total_kwh,
                    :estimated_cost)
            """, data)
            self._con.commit()
        except sqlite3.Error as err:
            print(err)

    def fetch_all(self):
        """ Fetch data from database
            
            Returns:
                dict: data from database
                bool: returns False if error
        """
        db = self._cur
        db.row_factory = sqlite3.Row
        try:
            db.execute("""
                SELECT * FROM usage_data
            """)
            desc = db.description
            column_names = [col[0] for col in desc]
            res = [dict(zip(column_names, row)) for row in db.fetchall()]
            return res
        except sqlite3.Error as err:
            print(err)
            return False

    def get_data(self, entity_id):
        """ Fetch data from database
            
            Returns:
                dict: data from database
                bool: returns False if error
        """
        db = self._cur
        try:
            db.execute("""
                SELECT *
                FROM usage_data
                WHERE entity_id LIKE ?
            """, (entity_id,))
            result = db.fetchall()
            return result
        except sqlite3.Error as err:
            print(err)
            return False

    def query_usage_data(self):
        """ Fetch usage data by device, day, and month

            Returns:
                dict: dictionary of data representations
                bool: returns False if error
        """
        db = self._cur
        qry_by_dev = """
                SELECT entity_id, SUM(estimated_cost) as total_by_device
                FROM usage_data
                GROUP BY entity_id
        """

        qry_by_date = """
                SELECT record_date, SUM(estimated_cost) as total_by_day
                FROM usage_data
                GROUP BY record_date
        """

        qry_by_usage = """
                SELECT entity_id, SUM(total_kwh) as total_by_kwh
                FROM usage_data
                GROUP BY entity_id
        """

        qry_by_month = """
                SELECT 
                    STRFTIME('%m', record_date) as month,
                    SUM(total_kwh) as total_by_kwh,
                    SUM(estimated_cost) as total_by_cost
                FROM usage_data
                GROUP BY month
        """

        try:
            db.execute(qry_by_dev)
            desc = db.description
            column_names = [col[0] for col in desc]
            dev_res = [dict(zip(column_names, row))
                       for row in db.fetchall()]

            db.execute(qry_by_date)
            desc = db.description
            column_names = [col[0] for col in desc]
            date_res = [dict(zip(column_names, row))
                       for row in db.fetchall()]

            db.execute(qry_by_usage)
            desc = db.description
            column_names = [col[0] for col in desc]
            kwh_res = [dict(zip(column_names, row))
                       for row in db.fetchall()]

            db.execute(qry_by_month)
            desc = db.description
            column_names = [col[0] for col in desc]
            month_res = [dict(zip(column_names, row))
                       for row in db.fetchall()]
        except sqlite3.Error as err:
            print(err)
            return False

        return {'BY DEVICE': dev_res, 'BY DATE': date_res, 'BY KWH': kwh_res, 'BY MONTH': month_res}

    @property
    def table(self):
        """ da table """
        return self._table

    @table.setter
    def table(self, table):
        """ Kinda don't like this """
        self._table = table

        table_qry ="""
                    CREATE TABLE IF NOT EXISTS usage_data (
                        record_date DATETIME NOT NULL,
                        entity_id TEXT NOT NULL,
                        total_kwh REAL,
                        estimated_cost REAL,
                        PRIMARY KEY(record_date, entity_id))
                    """
        self._con.execute(table_qry)
