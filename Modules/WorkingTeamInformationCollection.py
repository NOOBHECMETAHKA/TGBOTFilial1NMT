import pandas

class WorkingTeamInformation():
    def __init__(self, file_path_of_working_class=f"C:\\Users\\Sharpanskih\\Desktop\\Список рабочей команды.xlsx"):
        self.file_path_of_working_class = file_path_of_working_class
        self.dataframe_working_team = pandas.read_excel(self.file_path_of_working_class, engine='openpyxl', skiprows=1, sheet_name="Рабочка")
    
    def get_working_man_list_fio(self) -> list:
        df = self.dataframe_working_team
        return (df.iloc[:, 9].astype(str) + ' ' + df.iloc[:, 10].astype(str) + ' ' + df.iloc[:, 11].astype(str)).tolist()
    
    def find_working_man_from_working_team_by_fullname(self, FullName: str) -> pandas.DataFrame:
        dataFrame_working_team = self.dataframe_working_team
        dataFrame_working_team["FullName"] = dataFrame_working_team["Фамилия"] + " " + dataFrame_working_team["Имя"] + " " + dataFrame_working_team["Отчество"]
        return dataFrame_working_team[dataFrame_working_team["FullName"].str.contains(FullName, case=False)]
    
    def get_available_military_unit(self) -> list:
        return self.dataframe_working_team["В/Ч"].unique().tolist() 
    
    def find_working_man_from_working_team_by_military_unit_text_card(self, military_unit: str) -> str:
        buffer = str
        if military_unit in self.get_available_military_unit():
            df = self.dataframe_working_team
            df = df[df["В/Ч"] == military_unit]
            dict_coincidence = df.to_dict(orient="index")
            buffer = f"Рабочая команда в\ч: \n"
            if len(dict_coincidence) > 0:
                for index, person_index in enumerate(dict_coincidence):
                    person = dict_coincidence[person_index]
                    buffer += f"{index + 1}. {person["Фамилия"]} {person["Имя"]} {person["Отчество"]};\nРабочее место: {person["Место работы"]}; Место жительства: {person["Место жительства"]};\nДни в госпитале: {person["ГС дни"]} дней\n"
                buffer += f"*Количество совпадений: {len(dict_coincidence)}"
            else:
                buffer += "Ничего не нашлось. Сообщите об ошибке разработчику!"
        else:
            buffer = "Ничего не найдено! Убедитесь правильно ввели воинскую часть"
        return buffer
    
    def find_working_man_from_working_team_by_fullname_text_card(self, FullName: str) -> str:
        buffer = str
        df = self.find_working_man_from_working_team_by_fullname(FullName=FullName)
        dict_coincidence = df.to_dict(orient="index")
        buffer = "Предположительные варианты поиска:\n"
        if len(dict_coincidence) > 0 and len(dict_coincidence) <= 5:
            for index, person_index in enumerate(dict_coincidence):
                person = dict_coincidence[person_index]
                buffer += f"{index + 1}. {person["FullName"]};\nВоинская часть {person["В/Ч"]};\nРабочее место: {person["Место работы"]}; Место жительства: {person["Место жительства"]};\nДни в госпитале: {person["ГС дни"]} дней\n"
            buffer += f"*Количество совпадений: {len(dict_coincidence)}"
        elif len(dict_coincidence) > 5:
            for index, person_index in enumerate(dict_coincidence):
                buffer += f"{index + 1}. {dict_coincidence[person_index]["FullName"]}\n"
            buffer += f"*Количество совпадений: {len(dict_coincidence)}\n"
            buffer += "*Результат поиска больше 5 - добавьте больше значений для поиска!"
        else:
            buffer += "Ничего не найдено! Попробуй найти другое сочетание букв."
        return buffer
    
print(WorkingTeamInformation().find_working_man_from_working_team_by_military_unit_text_card(55591))