# """ Only for Kasa devices. Tapo will be next """
# import re
# import os
# import json
# from datetime import datetime
# from dotenv import load_dotenv
# from kasa import exceptions
# from modules import calculate_usage as cal

# DT_FORMAT = "%Y-%m-%d %H:%M:%S"
# load_dotenv()

# class KasaDevice:
#     """ Class to hold Kasa device info """
#     RECORD_START = "start"
#     RECORD_END = "end"

#     def __init__(self, device, device_name = " "):
#         self._dev = device
#         self.device_name = device_name
#         self.status = KasaDevice.RECORD_START

#     async def record_device_at_time(self):
#         """ Get device usage information at specified times """
#         file_path = f"{os.getenv('FILEPATH')}{self.device_name}.json"
#         start_date = datetime.now().replace(day=1, hour=6, minute=0, second=0, microsecond=0)
#         date_of_entry = datetime.now().strftime(DT_FORMAT)
#         try:
#             print(self.device_name)
#             usage = self._dev.modules.get("Energy")
#             print(type(usage))
#             print(await usage.get_daily_stats(year=2024, month=9))
#         except exceptions.KasaException as e:
#             # : Handle exception
#             print(e)

#         # res = {
#         #     'date_time': date_of_entry,
#         #     'device': self.device_name,
#         #     'wattage': usage.consumption_today,
#         #     'record_type': self.status
#         # }

#         # if os.path.exists(file_path):
#         #     with open(file_path, "r", encoding='utf-8') as fp:
#         #         data = json.load(fp)
#         #     data.append(res)
#         # else:
#         #     data = [res]

#         # with open(file_path, "w", encoding='utf-8') as fp:
#         #     json.dump(data, fp)

#     def fetch_usage_data(self):
#         """ Get usage data, and calculate total usage """
#         file_path = f"{os.getenv('FILEPATH')}{self.device_name}.json"
#         with open(file_path, "r", encoding='utf-8') as fp:
#             data = json.load(fp)

#         if self.status == KasaDevice.RECORD_END:
#             cal.calculate_daily_kwh(data=data)

#     def clear_json(self):
#         """ Just delete everything man """
#         file_path = f"{os.getenv('FILEPATH')}{self.device_name}.json"
#         with open(file_path, "w", encoding='utf-8') as w:
#             json.dump([],w)

#     @property
#     def device_name(self):
#         """ yee """
#         return self._device_name

#     @device_name.setter
#     def device_name(self, device_name):
#         try:
#             new_name = device_name.strip()
#             new_name = new_name.replace(" ", "_")
#             new_name = re.sub(r'\W+','', new_name)
#             new_name = new_name.lower()

#             self._device_name = new_name
#         except AttributeError as err:
#             print(err)
#             print("cannot do the name man")
