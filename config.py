import os

user = os.getlogin()

#Каталоги для подключения к базе данных
REF_TO_DATABASE = {
    "SERVER": "\\\\192.168.3.13\\DatabaseEx\\{0}",
    "ROOT_DIR": "C:\\DataBaseEX\\{0}",
    "TEST": f"C:\\Users\\{user}\\Desktop\\" + "{0}"
} 
#Файлы для подключения к базе данных
TITLE_DATABASE = {
    "INC": "Project_2010_Mail_Inc.accdb",
    "OCT": "Project_2010_Mail_Otc.accdb",
    "TEST": "test.accdb"
}
#Файл для подключения к файлу рабочей команды
FILE_WORKING_TEAM = f"C:\\Users\\{user}\\Desktop\\Список рабочей команды.xlsx"
