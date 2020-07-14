import logging

import re
import datetime
from pprint import pprint


class DpkgParser:
    def __init__(self, filepath, range_days, test_mode=False):
        self.unknown = []
        self.reinstall = []
        self.purge = []
        self.remove = []
        self.upgrade = []
        self.install = []
        self.filepath = filepath
        self.testMode = test_mode
        if range_days is not None:
            self.fromDate = datetime.datetime.today() - datetime.timedelta(days=range_days)
        else:
            self.fromDate = None
        self.parse()

    # Parse File
    def parse(self):

        with open(self.filepath) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                line = fp.readline()
                line = line.strip()
                if len(line.strip()) != 0:

                    date = line.split()[0]
                    time = line.split()[1]

                    date_time_obj = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
                    if self.fromDate is None or self.fromDate < date_time_obj:

                        if (line.split()[2] == "remove" or line.split()[2] == 'purge') and (
                                line.split()[4] != line.split()[4]) and (
                                len(line.split()) == 6 and re.match("/^<\w+>$/.*", line.split()[5])):
                            self.unknown.append(line)
                        elif "remove" == line.split()[2]:
                            self.remove.append(line.split()[3] + line.split()[4])
                        elif "purge" == line.split()[2]:
                            self.purge.append(line.split()[3] + line.split()[4])
                        elif len(line.split()) == 6 and re.match("[<>]", line.split()[5]):
                            self.install.append(line.split()[3] + ' ' + line.split()[4])
                        elif len(line.split()) == 6 and line.split()[5].find(':') != -1:
                            if not self.upgrade.__contains__(
                                    line.split()[3] + line.split()[4] + " => " + line.split()[5]):
                                self.upgrade.append(line.split()[3] + line.split()[4] + " => " + line.split()[5])
                cnt += 1

        self.install.sort()
        self.upgrade.sort()
        self.reinstall.sort()
        self.purge.sort()
        self.remove.sort()
        if not self.testMode:
            print("------------------DPKG----------------------------")
            print("Installed: ")
            for log in self.install:
                print('  ' + log)
            print("-----------------------")
            print("Removed: ")
            for log in self.remove:
                print('  ' + log)
            print("-----------------------")
            print("Upgraded: ")
            for log in self.upgrade:
                print('  ' + log)
            print("-----------------------")
            print("Purged: ")
            for log in self.purge:
                print('  ' + log)
            print("--------------END of DPKG-------------------------")

    def getLogs(self):
        return {'install': self.install,
                'upgrade': self.upgrade,
                'reinstall': self.reinstall,
                'purge': self.purge,
                'remove': self.remove
                }
