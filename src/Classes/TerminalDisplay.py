""" Output data to terminal """
import curses
import sys
import datetime as dt
from helpers.calculations import get_running_total as grt
from helpers.calculations import get_running_kwh_total as grkt

class TerminalDisplay:
    """ Class to handle outputting data to terminal """
    def __init__(self, rt_data, stats_data, entity_ids, current_data):
        self.entity_ids = entity_ids
        self.rt_data = rt_data
        self.stats_data = stats_data
        self.current_data = current_data
        self.buffer = len(entity_ids)
        self.scr = curses.initscr() if int(sys.argv[1]) < 2 else None

    def output_rt(self):
        """ Realtime output """
        strings = []
        title_string = 'DATE'.ljust(13) + 'DEVICE'.ljust(26) + 'KWH'.ljust(11) + 'RUNNING COST'
        self.scr.addstr(0,0, '%-10s' % title_string)
        for item in self.rt_data:
            item = grt(self.current_data, item)
            ts = TerminalStrings(item)
            strings.append(ts.data_string)
            for idx, val in enumerate(strings):
                self.scr.addstr(idx + 1, 0, '%-10s' % val)
                self.scr.refresh()

    def output_stats(self):
        """ Stats by different time frames """
        by_device = self.stats_data['BY KWH']
        by_date = self.stats_data['BY DATE']
        by_month = self.stats_data['BY MONTH']
        strings = []

        strings.append('TOTAL USAGE BY DEVICE')
        strings.append('DEVICE'.ljust(26) + 'KWH TOTAL')
        for item in by_device:
            item = grkt(self.rt_data, item)
            ts = TerminalStrings(item)
            strings.append(ts.data_string)
        strings.append('')
        strings.append('TOTAL COST BY DATE')
        strings.append('DATE'.ljust(26) + 'COST')

        for date in by_date:
            ts = TerminalStrings(date)
            strings.append(ts.data_string)

        strings.append('')
        strings.append('CONSUMPTION AND COST BY MONTH')
        for month in by_month:
            ts = TerminalStrings(month)
            strings.append(ts.data_string)

        buffer = self.buffer + 2

        for idx, val in enumerate(strings):
            self.scr.addstr(idx + buffer, 0, '%-10s' % val)
            self.scr.refresh()
class TerminalStrings:
    """ Class to handle string formatting """
    def __init__(self, data):
        self.device_name = data
        self.data_string = data

    @property
    def device_name(self):
        """Device name without the fluff"""
        return self._device_name

    @device_name.setter
    def device_name(self, data):
        self._device_name = ""
        try:
            self._device_name = (data['entity_id']
                                    .replace('sensor.', '')
                                    .replace('_today_s_consumption', '')
                                    .replace('_', ' ')
            )
        except KeyError:
            pass

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
        except KeyError:
            pass

        try:
            self._data_string = f'{self.device_name:<23s} | '\
                    f'{str(round(data['total_by_kwh'],5)):<23s}\n'
        except KeyError:
            pass

        try:
            self._data_string = f'{data['record_date']:<23s} | '\
                    f'${str(round(data['total_by_day'],5)):<23s}\n'
        except KeyError:
            pass

        try:
            month = int(data['month'])
            month_abrv = dt.datetime.now().replace(2024,month,1).strftime('%b')
            self._data_string = f'{month_abrv:<2s} | '\
                    f'{str(round(data['total_by_kwh'],5)):<6s} kwh | '\
                    f'${str(round(data['total_by_cost'],5))}\n'
        except KeyError:
            pass
