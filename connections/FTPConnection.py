from ftplib import FTP
import logging

class FTPConnection:
    def __init__(self, host, username, password, path, filename, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.path = path
        self.filename = filename
        self.port = port
        self.ftp = None
        self.tmpFile = '/tmp/tmpFTPLogs'

    def connect(self):
        try:
            self.ftp = FTP(self.host, self.username, self.password)
            self.ftp.cwd(self.path)
            logging.debug("FTP Connected")
        except:
            logging.critical("Could not connect to server")

    def getLogFile(self):
        if self.ftp is None:
            logging.critical("There is no ftp connection")
        try:
            file = open(self.tmpFile, 'wb')
            self.ftp.retrbinary("RETR " + self.filename, file.write)
            file.close()

        except:
            logging.error("Cannot download given file")

    def close(self):
        self.ftp.quit()
        logging.debug("FTP closed")
