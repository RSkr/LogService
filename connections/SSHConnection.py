import paramiko
import logging


class SSHConnection:
    def __init__(self, host, username, password, path, port):
        self.host = host
        self.username = username
        self.password = password
        self.path = path
        self.port = port
        self.ssh = paramiko.SSHClient()
        self.sftp = None
        self.tmpFile = '/tmp/tmpSSHLogs.txt'

    def connect(self):
        try:
            self.ssh.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)
            self.sftp = self.ssh.open_sftp()
            logging.debug("SSH connected")
        except:
            logging.critical("Could not connect to server")

    def getLogFile(self):
        if self.sftp is None:
            logging.critical("There is no ssh connection")

        try:
            self.sftp.get(self.path, self.tmpFile)

        except:
            logging.error("Cannot download given file")

    def close(self):
        self.ssh.close()
        logging.debug("SSH closed")
