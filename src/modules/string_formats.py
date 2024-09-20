def format_device_name(device_name) -> str:
    """TODO"""
    return (device_name
                .replace('sensor.', '')
                .replace('_today_s_consumption', '')
                .replace('_', ' '))

