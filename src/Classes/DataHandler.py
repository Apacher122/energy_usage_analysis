import datetime as dt
from Classes.db import Queries as qry
from Classes import HADevice as hd
from Classes.TerminalDisplay import TerminalDisplay

class DataHandler:
    def __init__(self, entities, current_data):
        self.rt_data = []
        self.stats_data = []
        self.past_data = []
        self.entity_ids = []
        self.current_data = current_data
        self.date_today = dt.datetime.now()
        self.device = None
        self.start_date = self.date_today
        self.end_date = self.date_today
        self.entities = entities
        self.db = qry.HAQueries(filename = 'usage.db')

    async def get_usage_data(self):
        self.rt_data = []
        for entity in self.entities:
            if ("today_s_consumption" in entity.entity_id and 
                "cost" not in entity.entity_id
            ):
                await entity.async_update_state()
                self.entity_ids.append(entity.entity_id)
                self.device = hd.HADevice(self.start_date.date(), entity)
                data = await self.device.get_usage_and_costs(self.start_date, self.end_date)
                self.rt_data.append(data)
        self.stats_data = self.device.fetch_usage_stats()
        terminal = TerminalDisplay(
            rt_data=self.rt_data,
            stats_data=self.stats_data,
            entity_ids=self.entity_ids,
            current_data=self.current_data
        )
        terminal.output_rt()
        terminal.output_stats()

    async def update_database(self):
        """TODO"""
        data = []
        today = dt.datetime.now().date()
        all_data = self.db.fetch_all()

        for data in all_data:
            last_date = dt.datetime.strptime(data['record_date'], "%Y-%m-%d").date()

        while last_date < today:
            start_time = dt.datetime(
                last_date.year,
                last_date.month,
                last_date.day,
                hour=6,
                minute=0,
                second=0
            )
            end_time = start_time.replace(hour=19, minute=59)
            for entity in self.entities:
                if "today_s_consumption" in entity.entity_id and "cost" not in entity.entity_id:
                    await entity.async_update_state()
                    self.entity_ids.append(entity.entity_id)
                    device = hd.HADevice(start_time.date(), entity)
                    res = await device.get_usage_and_costs(start_time, end_time, update=True)
                    data.append(res)
                    device.commit_data_to_db(data=data)
            last_date += dt.timedelta(days=1)