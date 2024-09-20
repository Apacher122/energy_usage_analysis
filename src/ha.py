"""_summary_"""
import os
import asyncio
import sys
import datetime as dt
import homeassistant_api as ha
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Classes.DataHandler import DataHandler
from Classes.db import Queries as qry

load_dotenv()

API_URI = "http://homeassistant.local:8123/api/"
TOKEN = os.getenv('HOMEASSISTANT_TOKEN')
CURRENT_DATA = qry.HAQueries(filename = 'usage.db').query_usage_data()

class MyHAData:
    """TODO"""
    def __init__(self, get_realtime = False, output_stats = False, update_db = False):
        self.date_handler = None
        self.get_realtime = get_realtime
        self.update_db = update_db
        self.date_today = dt.datetime.now()

    async def handle_device_data(self):
        """TODO"""
        client = ha.Client(API_URI, os.getenv('HOMEASSISTANT_TOKEN'), use_async=True)
        async with client:
                groups = await client.async_get_entities()
                sensor_group = groups['sensor'].entities
                # self.entities = sensor_group.values()
                self.date_handler = DataHandler(entities=sensor_group.values(), current_data=CURRENT_DATA)
                if not self.update_db:
                    await self.date_handler.get_usage_data()
                else:
                    pass
                    # await self.update_data()

async def main():
    print(f"Process started on {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
    scheduler = AsyncIOScheduler()

    match int(sys.argv[1]):
        case 0: #realtime
            my_device = MyHAData(get_realtime=True, output_stats=True)
            scheduler.add_job(my_device.handle_device_data, trigger='interval', seconds=1)
        case 1: #stats
            my_device = MyHAData(output_stats=True)
            scheduler.add_job(my_device.handle_device_data)
        case 2: #EOD stats
            my_device = MyHAData()
            scheduler.add_job(my_device.handle_device_data, trigger='cron', hour='20', minute='00', misfire_grace_time=3600)
        case 3: #UPDATE
            my_device = MyHAData(get_realtime=False, output_stats=False, update_db=True)
            scheduler.add_job(my_device.handle_device_data)
        case _:
            print(f"Wrong input. You Entered: {sys.argv[1]}")
    scheduler.start()

    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    asyncio.run(main())