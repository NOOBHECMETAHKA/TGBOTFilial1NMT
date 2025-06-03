import unittest
from config import *
from os import path
import pyodbc

class PreliminaryTesting(unittest.TestCase):
    def setUp(self):
        self.file_working_team = REF_TO_DATABASE["TEST"].format(TITLE_DATABASE["TEST"])
        self.file_database_manager = FILE_WORKING_TEAM
    
    
    def test_check_file_working_team(self):
        '''Проверяет местоположние файла рабочей команды'''
        self.assertTrue(path.exists(self.file_working_team), "Файл рабочки не найден!")
    
    def test_check_file_database(self):
        '''Проверяет местоположение файла базы данных'''
        self.assertTrue(path.exists(self.file_database_manager), "Файл базы данных не найден!")
    
    def test_check_necessary_database_drivers(self):
        '''Проверяет доступность необходимого драйвера для работы с базой данных'''
        necessary_driver = "Microsoft Access Driver (*.mdb, *.accdb)"
        driver_pack_pyobc = pyodbc.drivers()
        self.assertIn(necessary_driver, driver_pack_pyobc)

