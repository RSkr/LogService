import logging
import datetime
import re


class PostgresParser:
    def __init__(self, filepath, range_days, test_mode=False):
        self.error = []
        self.hint = []
        self.warning = []
        self.logs = []
        self.statement = []
        self.users = []
        self.testMode = test_mode
        self.filepath = filepath
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

                    if len(line.split()) < 2:
                        continue

                    date = line.split()[0]
                    time = line.split()[1]

                    if not re.match("(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3})", date + ' ' + time):
                        cnt += 1
                        continue

                    date_time_obj = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S.%f')
                    if self.fromDate is None or self.fromDate < date_time_obj:
                        if line.split()[4].find('@') != -1:
                            if not self.users.__contains__(line.split()[4]):
                                self.users.append(line.split()[4])
                            if line.split()[5] == "LOG:":
                                if not self.logs.__contains__(line.split(':', 4)[3]):
                                    self.logs.append(line.split(':', 4)[3])
                            if line.split()[5] == "ERROR:":
                                if not self.error.__contains__(line.split(':', 4)[3]):
                                    self.error.append(line.split(':', 4)[3])
                            if line.split()[5] == "STATEMENT:":
                                if not self.statement.__contains__(line.split(':', 4)[3]):
                                    self.statement.append(line.split(':', 4)[3])
                            if line.split()[5] == "HINT:":
                                if not self.hint.__contains__(line.split(':', 4)[3]):
                                    self.hint.append(line.split(':', 4)[3])
                            if line.split()[5] == "WARNING:":
                                if not self.warning.__contains__(line.split(':', 4)[3]):
                                    self.warning.append(line.split(':', 4)[3])
                        else:

                            if line.split()[4] == "LOG:":
                                if not self.logs.__contains__(line.split(':', 4)[3]):
                                    self.logs.append(line.split(':', 4)[3])
                            if line.split()[4] == "ERROR:":
                                if not self.error.__contains__(line.split(':', 4)[3]):
                                    self.error.append(line.split(':', 4)[3])
                            if line.split()[4] == "STATEMENT:":
                                if not self.statement.__contains__(line.split(':', 4)[3]):
                                    self.statement.append(line.split(':', 4)[3])
                            if line.split()[4] == "HINT:":
                                if not self.hint.__contains__(line.split(':', 4)[3]):
                                    self.hint.append(line.split(':', 4)[3])
                            if line.split()[4] == "WARNING:":
                                if not self.warning.__contains__(line.split(':', 4)[3]):
                                    self.warning.append(line.split(':', 4)[3])

                cnt += 1

        self.error.sort()
        self.statement.sort()
        self.logs.sort()
        self.warning.sort()
        self.hint.sort()
        self.users.sort()
        if not self.testMode:
            print("------------------PostgreSQL----------------------")
            print("Errors: ")
            for log in self.error:
                print(log)
            print("-----------------------")
            print("Statement: ")
            for log in self.statement:
                print(log)
            print("-----------------------")
            print("Hint: ")
            for log in self.hint:
                print(log)
            print("-----------------------")
            print("Log: ")
            for log in self.logs:
                print(log)
            print("-----------------------")
            print("Warning: ")
            for log in self.warning:
                print(log)
            print("-----------------------")
            print("Users: ")
            for log in self.users:
                print('  ' + log)
            print("--------------END of PostgreSQL-------------------")

    def getLogs(self):
        return {'error': self.error,
                'statement': self.statement,
                'logs': self.logs,
                'warning': self.warning,
                'hint': self.hint,
                'users': self.users
                }