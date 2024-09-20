import os
import datetime as dt
from helpers.calculations import get_running_total as grt
from Classes.db import Queries as qry
from dotenv import load_dotenv
load_dotenv


class MyDevices:
    """TODO"""
    def __init__(
        self,
        record_date = dt.datetime.now().date(),
        entity = None
    ):
        self.record_date = record_date
        self.entity = entity
        self.history = None
        self.start_kwh = 0.0
        self.end_kwh = 0.0
        self.db = qry.HAQueries(filename = 'usage.db', table=self.device_name)

    def commit_data_to_db(self, data):
        """TODO"""
        self.db.insert(data=data)

    def fetch_data_from_db(self, entity_id):
        """TODO"""
        return self.db.get_data(entity_id=entity_id)

    def fetch_usage_stats(self):
        """TODO"""
        return self.db.query_usage_data()
    
    def update_database(self):
        today = str(dt.datetime.now().date())
        [res] = self.db.fetch_all()
        if today in res.values():
            print("FOUND")
        else:
            print(res.values())

    @property
    def device_name(self):
        """TODO"""
        try:
            return self.entity.entity_id
        except TypeError:
            print("replace this")

class HADevice(MyDevices):
    """TODO"""

    def update_database(self):
        today = str(dt.datetime.now().date())
        [res] = self.db.fetch_all()
        if today in res.values():
            print("FOUND")
        else:
            print(res.values())

    async def get_usage_and_costs(self, start, end, update=False):
        """TODO"""
        today = dt.datetime.now()
        estimated_cost = 0.0

        if ((start >= today.replace(hour=6, minute=0, second=0) and
            end <= today.replace(hour=20,minute=00,second=00))
        ):
            start = today.replace(hour=6, minute=0,second=0)
            in_billable_window = True
        else:
            in_billable_window = False

        await self.get_history(start, end)
        print(self.device_name)

        try:
            print(self.start_kwh)

            start_val = float(self.start_kwh)
            end_val = float(self.end_kwh)
        except:
            print("oops")

        total_kwh = end_val - start_val

        if in_billable_window or update:
            estimated_cost = total_kwh * float(os.getenv('COST_PER_KWH'))
        else:
            in_billable_window = False

        data = {
            'record_date': self.record_date,
            'entity_id': self.device_name,
            'total_kwh': total_kwh,
            'estimated_cost': round(estimated_cost, 4)
        }

        return data

    async def get_updated_data(self):
        await self.entity.async_write_ha_state()

    async def get_history(self, start, end):
        """TODO"""
        self.history = await self.entity.async_get_history(start_timestamp=start, end_timestamp=end)
        if self.history is not None:
            self.start_kwh = self.history.states[0].state
            self.end_kwh = self.history.states[len(self.history.states) - 1].state