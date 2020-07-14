#!/usr/bin/python3

import sys
import logging
from connections.SSHConnection import SSHConnection
from connections.FTPConnection import FTPConnection
from connections.HTTPConnection import HTTPConnection
from connections.LocalConnection import LocalConnection
from parsers.CustomParser import CustomParser
from parsers.PostgresParser import PostgresParser
from parsers.DpkgParser import DpkgParser
from parsers.HttpParser import HttpParser
import yaml

HOST_HTTP = 'www'
HOST_SSH = 'localhost'
HOST_FTP = 'ftp'
HOST_LOCAL = 'localhost'

TYPE_HTTP = 'http'
TYPE_POSTGRES = 'postgres'
TYPE_DPKG = 'dpkg'
TYPE_CUSTOM = 'custom'

CONFIG_RANGE_DAYS = None

logging.basicConfig(filename='logs/logs.txt', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)-8s - %(filename)s:%(lineno)s - %(message)s')

if sys.version_info < (3, 6):
    print('Need to run in python min 3.6')
    sys.exit(-1)


def main():
    print('Logger v1.0.0')
    parseSettings()

    logging.debug('end')


def parseSettings():
    with open('settings.yaml') as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)

    for k in range(len(settings["connections"])):
        host = settings["connections"][k]['host']
        '''
        if host == HOST_SSH:
            logging.info('Getting ssh data')
            ssh = SSHConnection(
                settings["connections"][k]["path"],
                settings["connections"][k]["login"],
                settings["connections"][k]["password"],
                settings["connections"][k]["file"],
                settings["connections"][k]["port"]
            )
            ssh.connect()
            ssh.getLogFile()
            ssh.close()
            print("Analyzing file from SSH host - " + settings["connections"][k]['path'])
            parseFile(settings["connections"][k]["type"], ssh.tmpFile)
        '''
        if host == HOST_HTTP:
            logging.info('Getting www data')
            www = HTTPConnection(
                settings["connections"][k]['path'],
                settings["connections"][k]['login'],
                settings["connections"][k]['password']
            )
            www.connect()
            www.getLogFile()
            www.close()
            print("Analyzing log file from HTTP host - " + settings["connections"][k]['path'])
            parseFile(settings["connections"][k]["type"], www.tmpFile)

        if host == HOST_FTP:
            logging.info('Getting ftp data')
            ftp = FTPConnection(
                settings["connections"][k]['path'],
                settings["connections"][k]['login'],
                settings["connections"][k]['password'], '',
                settings["connections"][k]['file'])
            ftp.connect()
            ftp.getLogFile()
            ftp.close()
            print("Analyzing log file from FTP host - " + settings["connections"][k]['path'])
            parseFile(settings["connections"][k]["type"], ftp.tmpFile)
        
        if host == HOST_LOCAL:
            logging.info('Getting local data')
            local = LocalConnection(settings["connections"][k]["path"])
            local.connect()
            local.close()
            print("Analyzing log file from local storage")
            parseFile(settings["connections"][k]["type"], local.path)



def parseFile(type, filePath):
    if type == TYPE_HTTP:
        return HttpParser(filePath, CONFIG_RANGE_DAYS)
    if type == TYPE_POSTGRES:
        return PostgresParser(filePath, CONFIG_RANGE_DAYS)

    if type == TYPE_DPKG:
        return DpkgParser(filePath, CONFIG_RANGE_DAYS)

    if type == TYPE_CUSTOM:
        return CustomParser(filePath, CONFIG_RANGE_DAYS)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv.__contains__("-v"):
        logFormatter = logging.Formatter(" %(asctime)s - %(levelname)-8s - %(message)s")
        rootLogger = logging.getLogger()
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)
    elif len(sys.argv) > 2 and sys.argv.__contains__('-days'):
        if not sys.argv[sys.argv.index('-days') + 1].isnumeric() or int(sys.argv[sys.argv.index('-days') + 1]) < 0:
            print("Dni muszą bić liczbą większą od 0!")
            exit()
        CONFIG_RANGE_DAYS = int(sys.argv[sys.argv.index('-days') + 1])
    main()
