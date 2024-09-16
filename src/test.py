"""Main app"""
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from modules import device_manager as dm
from Classes import KasaDevice as dv

DT_FORMAT = "%Y-%m-%d %H:%M:%S"
class DeviceUsage:
    """Fetch devices, get usage stats"""

    def __init__(self, devices):
        self.devices = devices

    async def get_usage_data(self, dev, period):
        """Fetch usage data from devices

        Args:
            dev (Device): python-kasa Class
            period (str): start or end of record period
        """

        print("Fetching Usage Data at: " + datetime.now().strftime(DT_FORMAT), end='\r')
        await dev.update()
        device = dv.KasaDevice(device = dev, device_name = dev.alias)
        device.status = period
        await device.record_device_at_time()
        if period == device.RECORD_END:
            device.fetch_usage_data()
            await dev.disconnect()

    async def fetch_all_devices(self, period):
        """Create concurrent tasks for each device

        Args:
            period (str): start or end of record period
        """

        tasks = [self.get_usage_data(dev, period) for dev in self.devices.values()]
        await asyncio.gather(*tasks)

    def set_up(self, period):
        """Set up
        
        Args:
            period (str): start or end of record period
        """

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.ensure_future(self.fetch_all_devices(period))
        loop.run_until_complete(future)
        loop.close()

async def main():
    """Schedule start and end recording sessions"""

    print("fetching devices...")
    devices = await dm.fetch_devices()
    device_usage = DeviceUsage(devices=devices)
    print("done.")
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        device_usage.set_up,
        args=[dv.KasaDevice.RECORD_START],
        trigger='cron',
        hour='06',
        minute='00'
    )

    scheduler.add_job(
        device_usage.set_up,
        args=[dv.KasaDevice.RECORD_END]
    )

    scheduler.print_jobs()
    scheduler.start()

    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        for  dev in device_usage.devices.values():
            await dev.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
