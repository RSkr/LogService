#!/usr/bin/python3
import os
import unittest

from connections.FTPConnection import FTPConnection
from connections.HTTPConnection import HTTPConnection
from connections.LocalConnection import LocalConnection
from connections.SSHConnection import SSHConnection
from parsers.DpkgParser import DpkgParser
from parsers.PostgresParser import PostgresParser
from parsers.HttpParser import HttpParser


class LogServiceTestCases(unittest.TestCase):

    def setUp(self):
        self.test = 5
    
    def test_dpkg_all_range_parser(self):
        parser = DpkgParser("test/logs/dpkg.log", None, True)
        self.assertEqual(len(parser.getLogs()['install']), 447)
        self.assertEqual(len(parser.getLogs()['reinstall']), 0)
        self.assertEqual(len(parser.getLogs()['purge']), 5)
        self.assertEqual(len(parser.getLogs()['remove']), 15)

    def test_dpkg_30_days_range_parser(self):
        parser = DpkgParser("test/logs/dpkg.log", 30, True)
        self.assertEqual(len(parser.getLogs()['install']), 41)
        self.assertEqual(len(parser.getLogs()['reinstall']), 0)
        self.assertEqual(len(parser.getLogs()['purge']), 0)
        self.assertEqual(len(parser.getLogs()['remove']), 0)

    def test_postgres_all_range_parser(self):
        parser = PostgresParser("test/logs/postgresql-10-main.log", None, True)
        self.assertEqual(len(parser.getLogs()['error']), 49)
        self.assertEqual(len(parser.getLogs()['warning']), 1)
        self.assertEqual(len(parser.getLogs()['statement']), 67)
        self.assertEqual(len(parser.getLogs()['hint']), 3)
        self.assertEqual(len(parser.getLogs()['users']), 3)

    def test_postgres_60_days_range_parser(self):
        parser = PostgresParser("test/logs/postgresql-10-main.log", 30, True)
        self.assertEqual(len(parser.getLogs()['error']), 7)
        self.assertEqual(len(parser.getLogs()['warning']), 1)
        self.assertEqual(len(parser.getLogs()['statement']), 13)
        self.assertEqual(len(parser.getLogs()['hint']), 1)
        self.assertEqual(len(parser.getLogs()['users']), 2)
    
    def test_http_all_range_parser(self):
        parser = HttpParser("test/logs/http.log", None, True)
        self.assertEqual((parser.getLogs()['lines']), 128062)
        self.assertEqual((parser.getLogs()['codes']), 15)
        self.assertEqual((parser.getLogs()['statusError']), 43796)
    
    def test_http_30_days_range_parser(self):
        parser = HttpParser("test/logs/http.log", 30, True)
        self.assertEqual((parser.getLogs()['lines']), 61518)
        self.assertEqual((parser.getLogs()['codes']), 14)
        self.assertEqual((parser.getLogs()['statusError']), 40668)

    
    def test_ssh_connection(self):
        ssh = SSHConnection(
            'localhost',
            'logger',
            'logger_password',
            'dpkg.log',
            '2222'
        )
        ssh.connect()
        ssh.getLogFile()
        ssh.close()
        self.assertTrue(os.path.exists(ssh.tmpFile))


    def test_ftp_connection(self):
        ftp = FTPConnection(
            'ftp.estelladandyk.kylos.pl',
            'logger@estelladandyk.kylos.pl',
            'y^sAr~j29=pr', '',
            'file.txt')
        ftp.connect()
        ftp.getLogFile()
        ftp.close()
        self.assertTrue(os.path.exists(ftp.tmpFile))


    def test_http_connection(self):
        www = HTTPConnection(
            'http://estelladandyk.kylos.pl/logger/file.txt',
            'logger',
            'logger_password'
        )
        www.connect()
        www.getLogFile()
        www.close()
        self.assertTrue(os.path.exists(www.tmpFile))

    
    def test_localhost_connection(self):
        local = LocalConnection('test/logs/postgresql-10-main.log')
        local.connect()
        local.close()
        # self.assertTrue(os.path.exists(local.tmpFile))
    
if __name__ == '__main__':
    unittest.main()