import logging

from pip._vendor import requests


class HTTPConnection:
    def __init__(self, host, login, passwd):
        self.host = host
        self.www = None
        self.tmpFile = r'/tmp/tmpWWWLogs'
        self.login = login
        self.passwd = passwd

    def connect(self):
        logging.debug("WWW Connected")

    def getLogFile(self):
        try:
            response = requests.get(self.host, auth=(self.login, self.passwd))
            file = open(self.tmpFile, 'w')
            file.write(str(response.text))
            file.close()
            logging.debug('Successfully downloaded file')
            return self.tmpFile
        except:
            logging.critical("Cannot download file from www")

    def close(self):
        logging.debug('WWW closed')
