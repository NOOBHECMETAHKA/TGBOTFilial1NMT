import unittest
import pyodbc
import os.path as fileManager
from Modules.WorkingTeamInformationCollection import WorkingTeamInformation
from Modules.DataBaseManager import DataBaseManager

class PreliminaryTesting(unittest.TestCase):
    def setUp(self):
        self.file_working_team = WorkingTeamInformation().file_path_of_working_class
        self.file_database_manager = DataBaseManager().MAIN_PATH
    
    
    def test_check_file_working_team(self):
        '''Проверяет местоположние файла рабочей команды'''
        self.assertTrue(fileManager.exists(self.file_working_team), "Файл рабочки не найден!")
    
    def test_check_file_database(self):
        '''Проверяет местоположение файла базы данных'''
        self.assertTrue(fileManager.exists(self.file_database_manager), "Файл базы данных не найден!")
    
    def test_check_necessary_database_drivers(self):
        '''Проверяет доступность необходимого драйвера для работы с базой данных'''
        necessary_driver = "Microsoft Access Driver (*.mdb, *.accdb)"
        driver_pack_pyobc = pyodbc.drivers()
        self.assertIn(necessary_driver, driver_pack_pyobc)
    

#python -m unittest test.py  
