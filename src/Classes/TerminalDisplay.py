import curses
import sys
from Classes.TerminalStrings import TerminalStrings as TS
from helpers.calculations import get_running_total as grt

class TerminalDisplay:
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
            ts = TS(item)
            strings.append(ts.data_string)
            for idx, val in enumerate(strings):
                    self.scr.addstr(idx + 1, 0, '%-10s' % val)
                    self.scr.refresh()

    def output_stats(self):
        by_device = self.stats_data['BY DEVICE']
        by_date = self.stats_data['BY DATE']
        strings = []

        strings.append('TOTAL USAGE BY DEVICE')
        strings.append('DEVICE'.ljust(26) + 'KWH TOTAL')
        
        for item in by_device:
            ts = TS(item)
            strings.append(ts.data_string)
        
        strings.append('\nTOTAL USAGE BY DATE')
        strings.append('DATE'.ljust(26) + 'KWH TOTAL')
        
        for date in by_date:
            ts = TS(date)
            strings.append(ts.data_string)
        
        buffer = self.buffer + 2
        
        for idx, val in enumerate(strings):
            self.scr.addstr(idx + buffer, 0, '%-10s' % val)
            self.scr.refresh()