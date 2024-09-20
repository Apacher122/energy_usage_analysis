class TerminalStrings:
    def __init__(self, data):
        self.device_name = data
        self.data_string = data

    @property
    def device_name(self):
        """Device name without the fluff"""
        return self._device_name

    @device_name.setter
    def device_name(self, data):
        try:
            self._device_name = (data['entity_id']
                                    .replace('sensor.', '')
                                    .replace('_today_s_consumption', '')
                                    .replace('_', ' ')
            )
        except:
            self._device_name = ""

    @property
    def data_string(self):
        """Device output string"""
        return self._data_string

    @data_string.setter
    def data_string(self, data):
        self._data_string = ""
        try:
            self._data_string = f'{data['record_date']} | '\
                    f'{self.device_name:<23s} | '\
                    f'{data['total_kwh']:<2f} | '\
                    f'${round(data['estimated_cost'], 4)}'
        except:
            pass

        try:
            self._data_string = f'{self.device_name:<23s} | '\
                    f'{str(round(data['total_by_device'],5)):<23s}\n'
        except:
            pass

        try:
            self._data_string = f'{data['record_date']:<23s} | '\
                    f'{str(round(data['total_by_day'],5)):<23s}\n'
        except:
            print("OOOOOOOPS")
