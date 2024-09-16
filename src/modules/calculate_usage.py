""" This will handle monthly, weekly, and daily calculations (i.e. total kwh, cost for energy) """
import json
import os
from datetime import datetime as dt
from dotenv import load_dotenv

load_dotenv()

def calculate_kwh(data):
    """ 
        This will eventually handle multiple datapoints throughout the day.
        Goal is to use a left riemann sum to get hourly kwh. Might be more accurate
        than data presented from the Kasa app.
    """
    delta_t = 1/3600
    upper_limit = 0.0

    if len(data) < 3600:
        upper_limit = len(data)
    else:
        upper_limit = 3600

    kwh_summation = 0.0

    for n in range(0, upper_limit):
        kwh_summation += data[n]

    return delta_t * kwh_summation

def calculate_daily_cost(device_name, date_of_record, total_kwh):
    """ Calculate how much money I burnt to fist-fight the sun (using my ac)

    Args:
        device_name (str): device name
        date_of_record (str): year-month-day of record
        total_kwh (float): total usage over a specific timeframe =
    """
    cost_per_kwh = float(os.getenv('COST_PER_KWH'))
    res = [{
        "date_of_record": date_of_record,
        "device_name": device_name,
        "total_daily_cost": total_kwh * cost_per_kwh
    }]

    monthly_data_path =f"{os.getenv('FILEPATH')}monthly_costs\\{device_name}.json"

    if os.path.exists(monthly_data_path):
        with open(monthly_data_path, "r", encoding='utf-8') as fp:
            data = json.load(fp)
        data.append(res)
    else:
        data = [res]

    with open(monthly_data_path, "w", encoding='utf-8') as fp:
        json.dump(res, fp)

def calculate_daily_kwh(data):
    """ Get usage total between timeframe of a day

    Args:
        data (dict): holds all the recorded date for that day
    """

    print("Calculating kwh usage")
    start_kwh = 0.0
    end_kwh = 0.0
    start_recorded = False
    start_date = dt.now().date()
    print(data)
    for d in data:
        print(d)
        datetime = dt.strptime(d['date_time'], "%Y-%m-%d %H:%M:%S")
        record_date = datetime.date()
        record_type = d['record_type']

        if record_type == "start":
            print(F"Start: {d['date_time']}")
            start_kwh = d['wattage']
            start_recorded = True
            start_date = record_date

        if (record_type == "end" and
            start_date == record_date and
            start_recorded
        ):
            print(F"End: {d['date_time']}")
            end_kwh = d['wattage']
            print(end_kwh - start_kwh)

            calculate_daily_cost(
                device_name = d['device'],
                date_of_record = record_date.strftime('%Y-%m-%d'),
                total_kwh = end_kwh - start_kwh)
            start_kwh = 0.0
            end_kwh = 0.0
            start_recorded = False
