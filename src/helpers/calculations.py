""" Calculations buddy ol' pal"""
def get_running_total(past_data, cur_device):
    """ Calculate usage cost by device in real-time

    Args:
        past_data (dict): historical device data
        cur_device (dict): current device data

    Returns:
        dict: device with updated (real-time) data
    """
    device_stats = past_data['BY DEVICE']
    for device in device_stats:
        if cur_device['entity_id'] == device['entity_id']:
            cur_device['estimated_cost'] = round(cur_device['estimated_cost'], 4)
            cur_device['estimated_cost'] += round(device['total_by_device'], 4)

    return cur_device

def get_running_kwh_total(past_data, cur_device):
    """ Calculate usage over time by device in real-time

    Args:
        past_data (dict): historical device data
        cur_device (dict): current device data

    Returns:
        dict: device with updated (real-time) data
    """
    for device in past_data:
        if cur_device['entity_id'] == device['entity_id']:
            cur_device['total_by_kwh'] = round(cur_device['total_by_kwh'], 4)
            cur_device['total_by_kwh'] += round(device['total_kwh'], 4)

    return cur_device
