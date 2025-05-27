import pyodbc
import pandas
from datetime import datetime, timedelta 
from Modules.WorkingTeamInformationCollection import WorkingTeamInformation

class DataBaseManager:
    #Каталоги для подключения к базе данных
    REF_TO_DATABASE = {
        "SERVER": "\\\\192.168.3.13\\DatabaseEx\\{0}",
        "ROOT_DIR": "C:\\DataBaseEX\\{0}",
        "TEST": f"C:\\Users\\Sharpanskih\\Desktop\\" + "{0}"
    } 
    #Файлы для подключения к базе данных
    TITLE_DATABASE = {
        "INC": "Project_2010_Mail_Inc.accdb",
        "OCT": "Project_2010_Mail_Otc.accdb",
        "TEST": "test.accdb"
    }
    

    def __init__(self, ref="SERVER", name="OCT"):
        #Постоянный подключения к базу данных
        self.MAIN_PATH = self.REF_TO_DATABASE[ref].format(self.TITLE_DATABASE[name])
    

    #Получения DataFrame для дальнейшей обработки информации
    def connection_access_database(self, request: str) -> pandas.DataFrame:
        try:
            connection_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            connection_str += "DBQ={0};".format(self.MAIN_PATH)
            connection_to_database = pyodbc.connect(connection_str)
            data = pandas.read_sql(request, connection_to_database)
            return data
        
        except pyodbc.Error as e:
            print("Ошибка подключения: ", e)
            pass
        except pandas.errors.DatabaseError as e:
            print("Ошибка ошибка в запрос к базе данных: ", e)
        finally:
            if not connection_to_database.closed:
                connection_to_database.close()
    
    def select_from_year_OCT(self, year=datetime.now().year) -> pandas.DataFrame:
        """
        Получения данных от заданного года. Возвращает dataFrame.
        """
        query = f'SELECT * FROM [Основная таблица выписки] WHERE ((([Основная таблица выписки].[Дата поступления])>=#1/1/{year}#)) ORDER BY [Основная таблица выписки].[Дата поступления] DESC;'
        buffer = self.connection_access_database(query)
        return buffer
    
    def select_from_year_contengent_OCT(self, year=datetime.now().year) -> pandas.DataFrame:
        """
        Получения контенгента типа: "По призыву" от заданного года. Возвращает dataFrame.
        """
        buffer = self.select_from_year_OCT(year)
        buffer = buffer[buffer["Контингент"] == "По призыву"]
        return buffer
    
    def select_for_scout_contengent_format_FIO_Date(self, target_date=datetime.combine(date=datetime.today(), time=datetime.min.time())):
        workining_team = WorkingTeamInformation().get_working_man_list_fio()
        period_of_time = 1

        if target_date.weekday() == 0:
            period_of_time = 0
        elif target_date.weekday() == 6:
            period_of_time = 2

        query = 'SELECT [Основная таблица выписки].[Поступление-Отделение], [Основная таблица выписки].[Поcтупление-Койка], [Основная таблица выписки].Фамилия, [Основная таблица выписки].Имя, [Основная таблица выписки].Отчество, [Основная таблица выписки].[Дата выписки], [Основная таблица выписки].Контингент FROM [Основная таблица выписки] ORDER BY [Основная таблица выписки].[Дата выписки] DESC;'
        buffer = self.connection_access_database(query)
        buffer = buffer[buffer["Дата выписки"] >= (target_date - timedelta(days=period_of_time))]
        buffer = buffer[buffer["Контингент"] >= "По призыву"]

        buffer["Фамилия"] = buffer["Фамилия"].str.strip()
        buffer["Имя"] = buffer["Имя"].str.strip()
        buffer["Отчество"] = buffer["Отчество"].str.strip()

        buffer["Полное ФИО"] = buffer["Фамилия"] + " " + buffer["Имя"] + " " + buffer["Отчество"]
        buffer = buffer[buffer["Полное ФИО"].isin(workining_team)]
        
        formatted_sheet = ""

        formatted_sheet += f"Список выписанной рабочки\n"
        for unique_date in buffer["Дата выписки"].unique().tolist():
            formatted_sheet += f"По следующей дате: {unique_date.strftime('%d.%m.%Y')}\n"
            specific_formatted = buffer[buffer["Дата выписки"] == unique_date]
            for index_row, formatted_row in enumerate(specific_formatted.iloc[:, 7].astype(str) + ' | Дата выписки:  ' + specific_formatted.iloc[:, 5].dt.strftime('%d.%m.%Y').tolist()):
                formatted_sheet += f"{index_row + 1}. {formatted_row}\n"
        return formatted_sheet
    
    
    
    

    
