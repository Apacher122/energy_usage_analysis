import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
from modules import device_manager as dm
from Classes import Device as dv
from datetime import datetime

dt_format = "%Y-%m-%d %H:%M:%S"
scheduler = AsyncIOScheduler()

class DeviceUsage:
    def __init__(self, devices):
        self.devices = devices

    async def get_usage_data(self, dev, period):
        print("Fetching Usage Data at: " + datetime.now().strftime(dt_format), end='\r')
        await dev.update()
        device = dv.Device(device = dev, device_name = dev.alias)
        device.status = period
        await device.record_device_at_time()
        if period == device.RECORD_END:
            device.fetch_usage_data()
        await dev.disconnect()

    async def fetch_all_devices(self, period):
        tasks = [self.get_usage_data(dev, period) for dev in self.devices.values()]
        await asyncio.gather(*tasks)

    def set_up(self, period):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.ensure_future(self.fetch_all_devices(period))
        loop.run_until_complete(future)


    async def fetch_devices():
        print("fetching devices...")
        devices = await dm.fetch_devices()
        print("done.")

async def main():
    print("fetching devices...")
    devices = await dm.fetch_devices()
    device_usage = DeviceUsage(devices=devices)
    print("done.")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(device_usage.set_up, args=[dv.Device.RECORD_START], trigger='cron', hour='06', minute='00')
    scheduler.add_job(device_usage.set_up, args=[dv.Device.RECORD_END], trigger='cron', hour='19', minute='59')
    scheduler.start()

    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    asyncio.run(main())