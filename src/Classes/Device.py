from Classes.db import Queries as qry
from datetime import datetime
from dotenv import load_dotenv
from modules import calculate_usage as cal
import re
import os
import json

START = "start"
END = "end"
dt_format = "%Y-%m-%d %H:%M:%S"
load_dotenv()

class Device:
    RECORD_START = "start"
    RECORD_END = "end"

    def __init__(self, device, device_name = " "):
        self._dev = device
        self.device_name = device_name
        self._db = self.get_device_db()
        self.status = Device.RECORD_START

    def get_device_db(self):
        return qry.UsageQueries(filename = 'devices.db', table=self._device_name)
    
    async def record_device_at_time(self):
        file_path = f"{os.getenv('FILEPATH')}{self.device_name}.json"
        date_of_entry = datetime.now().strftime(dt_format)
        try:
            usage = self._dev.modules.get("Energy")
        except:
            print("oops")
        res = {
            'date_time': date_of_entry,
            'device': self.device_name,
            'wattage': usage.consumption_today
        }

        if os.path.exists(file_path):
            with open(file_path, "r") as fp:
                data = json.load(fp)
            data.append(res)
        else:
            data = [res]
        
        with open(file_path, "w") as fp:
            json.dump(data, fp)

    def fetch_usage_data(self):
        file_path = f"{os.getenv('FILEPATH')}{self.device_name}.json"
        with open(file_path, "r") as fp:
                data = json.load(fp)
        
        if self.status == Device.RECORD_END:
            cal.calculate_daily_kwh(data=data)

    def clear_json(self):
        file_path = f"{os.getenv('FILEPATH')}{self.device_name}.json"
        with open(file_path, "w") as w:
            data = json.dump([],w)


    @property
    def device_name(self): return self._device_name

    @device_name.setter
    def device_name(self, device_name):
        try:
            new_name = device_name.strip()
            new_name = new_name.replace(" ", "_")
            new_name = re.sub(r'\W+','', new_name)
            new_name = new_name.lower()

            self._device_name = new_name
        except:
            print("cannot do the name man")
