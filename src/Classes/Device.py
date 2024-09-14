from Classes.db import Queries as qry
from datetime import datetime

import re

dt_format = "%Y-%m-%d %H:%M:%S"

class Device:
    def __init__(self, device, device_name):
        self._dev = device
        self.device_name = device_name
        self._db = self.get_device_db()

    def get_device_db(self):
        return qry.UsageQueries(filename = 'devices.db', table=self._device_name)
    
    async def record_device(self):
        for i in range(10):
            await self._dev.update()
            time = datetime.now().strftime(dt_format)
            wattage = self._dev.features["current_consumption"].value

    @property
    def device_name(self): return self._device_name

    @device_name.setter
    def device_name(self, device_name):
        new_name = device_name.strip()
        new_name = new_name.replace(" ", "_")
        new_name = re.sub(r'\W+','', new_name)
        new_name = new_name.lower()

        self._device_name = new_name
        print(self._device_name)