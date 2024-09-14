

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