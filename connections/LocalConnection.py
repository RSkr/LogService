import os
import logging

class LocalConnection:
    def __init__(self, path):
        self.path = path

    def connect(self):
        logging.debug("Local connected")

    def getLogFile(self):
        if os.path.exists(self.path):
            try:
                file = open(self.path, 'r')
                file.close()
                return self.path;
            except:
                logging.error('Cannot open file: ' + self.path)
        else:
            logging.critical("Local file is unreachable")

    def close(self):
        logging.debug('Local closed')
