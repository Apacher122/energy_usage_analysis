def get_running_total(past_data, cur_device):
        """TODO"""
        device_stats = past_data['BY DEVICE']
        for device in device_stats:
            if cur_device['entity_id'] == device['entity_id']:
                cur_device['estimated_cost'] = round(cur_device['estimated_cost'], 4)
                cur_device['estimated_cost'] += round(device['total_by_device'], 4)

        return cur_device