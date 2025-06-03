import pyodbc, pandas
from datetime import datetime, timedelta 
from Modules.WorkingTeamInformationCollection import WorkingTeamInformation
from config import REF_TO_DATABASE, TITLE_DATABASE

class DataBaseManager:
    def __init__(self, ref="SERVER", name="TEST"):
        #Постоянный подключения к базу данных
        self.MAIN_PATH = REF_TO_DATABASE[ref].format(TITLE_DATABASE[name])

    #Получения DataFrame для дальнейшей обработки информации
    def connection_access_database(self, request: str) -> pandas.DataFrame:
        try:
            print(self.MAIN_PATH)
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
    
    def select_oct_contengent_for_military_unit(self, military_number, target_date=datetime.combine(date=datetime.today(), time=datetime.min.time())):
        df = self.select_from_year_OCT()
        workining_team = WorkingTeamInformation().get_working_man_list_fio()

        target_date = datetime(2025, 5, 22)

        df["ФИО"] = df["Фамилия"].str.strip() + " " + df["Имя"].str.strip() + " " + df["Отчество"].str.strip()
        df = df[df["Войсковая часть"] == f"{military_number}"]
        df = df[df["Дата выписки"] >= target_date]

        df_with_working_team = (df[df["ФИО"].isin(workining_team)]).to_dict(orient="index")
        df_with_out_working_team = (df[~df["ФИО"].isin(workining_team)]).to_dict(orient="index")

        buffer = ""
        buffer += "Список:\n"
        if len(df_with_out_working_team) > 0:
            for num, index_person in enumerate(df_with_out_working_team):
                person = df_with_out_working_team[index_person]
                buffer += f"{num + 1}. Дата поступления: {person["Дата поступления"].strftime('%d.%m.%Y')}; Дата выписки: {person["Дата выписки"].strftime('%d.%m.%Y')}; Направление: {(person["Направление выписки"])}{(" : " + person["В Другое ЛПУ"]) if (person["В Другое ЛПУ"]) is not None else ""}; {person["Воинское звание"]} {person["ФИО"]}; Диагноз: {person["Диагноз"]}\n"
        else:
            buffer += "Выписанных нету\n"

        buffer += "Список с рабочей командой:\n"
        if len(df_with_working_team) > 0:
            for num, index_person in enumerate(df_with_working_team):
                person = df_with_working_team[index_person]
                buffer += f"{num + 1}. Дата поступления: {person["Дата поступления"].strftime('%d.%m.%Y')}; Дата выписки: {person["Дата выписки"].strftime('%d.%m.%Y')}; Направление: {(person["Направление выписки"])}{(" : " + person["В Другое ЛПУ"]) if (person["В Другое ЛПУ"]) is not None else ""}; {person["Воинское звание"]} {person["ФИО"]}; Диагноз: {person["Диагноз"]}\n"
        else:
            buffer += "Выписанных нету\n"

        return buffer


    
    
    

    
