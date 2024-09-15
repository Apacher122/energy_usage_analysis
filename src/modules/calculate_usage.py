from datetime import datetime as dt
from datetime import timedelta as delta

def calculate_kwh(data):
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

def calculate_daily_kwh(data):
    print("Calculating kwh usage")
    for d in data:
        datetime = dt.strptime(d['date_time'], "%Y-%m-%d %H:%M:%S")
        start = datetime.now()
        record_start = datetime.replace(hour=6,minute=0)
        record_end = datetime.replace(hour=19,minute=59)
        buffer = delta(minutes=5)
        start_data = 0.0
        end_data = 0.0

        if (datetime.time() > (record_start - buffer).time() and 
            datetime.time() < (record_start + buffer).time()
            ):
            start = datetime
            print(F"Start: {d['date_time']}")
            start_data = d['wattage']

        if (datetime.date() == start.date() and
            datetime.time() < (record_end + buffer).time() and
            datetime.time() > (record_end - buffer).time()):
            print(F"End: {d['date_time']}")
            end_data = d['wattage']  
            print(end_data - start_data)

