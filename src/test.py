import asyncio
import json
from modules import device_manager as dm
from Classes.db import Queries as qry
from Classes import Device as dv
from kasa import SmartPlug
from datetime import datetime

dt_format = "%Y-%m-%d %H:%M:%S"

async def get_usage_date(dev):
    await dev.update()
    device = dv.Device(device=dev, device_name=dev.alias)
    db = qry.UsageQueries(filename = 'devices.db', table = dev.alias)
    data = []
    while True:
        for i in range(2):
            await dev.update()
            time = datetime.now().strftime(dt_format)
            device = dev.alias
            wattage = dev.features["current_consumption"].value
            if dev.alias == "Air conditioner":
                print(f'"date_time": {time}, "device": {device}, "wattage": {wattage}')
            data.append({"date_time": time, "device": device, "wattage": wattage})
            await asyncio.sleep(1)

        db.insert(data=data)
    await dev.disconnect()

async def main():
    devices = await dm.fetch_devices()
    tasks = [get_usage_date(dev) for dev in devices.values()]
    await asyncio.gather(*tasks)
    


if __name__ == "__main__":
    asyncio.run(main())