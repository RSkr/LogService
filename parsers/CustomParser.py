
import re
import datetime


class CustomParser:
    def __init__(self, filepath, range_days, test_mode=False):
        self.filepath = filepath
        self.testMode = test_mode
        if range_days is not None:
            self.fromDate = datetime.datetime.today() - datetime.timedelta(days=range_days)
        else:
            self.fromDate = None
        self.parse()

    # Define parser here
    def parse(self):
        with open(self.filepath) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                line = fp.readline()
                line = line.strip()
                if len(line.strip()) != 0:
                    print(line)
                    # parser body here

                cnt += 1
        return

    # return logs for unit testing
    def getLogs(self):
        return
