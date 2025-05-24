import os 
from telebot import types, TeleBot
from Modules.DataBaseManager import DataBaseManager
from Modules.WorkingTeamInformationCollection import WorkingTeamInformation

class TGNavigationMenuManager:
    def __init__(self):
        self.navIndex = 0
        self.main_menu_content = {
            0: {
                "flew_row": 1,
                "menu": [
                    "Выписка", #Ready
                    "Рабочка", #Ready
                    "Поиск по базе", #Ready 
                    "Выключение устройства" #Ready
                ]
            },
            1: {
                "flew_row": 1,
                "menu": [
                    "Плановое выключение через час", #Ready
                    "Плановое выключение через 20 минут", #Ready
                    "Отмена выключения", #Ready
                    "Выход" #Ready
                ]
            },
            2: {
                "flew_row": 1,
                "menu": [
                    "Выписка рабочей команды (Плановая)",#Ready
                    "Выписка части (Плановая)",
                    "Выход",#Ready
                ]
            },
            3: {
                "flew_row": 1,
                "menu": [
                    "Получить файл рабочей команды",
                    "Получить список для построяния",
                    "Найти рабочку по ФИО",
                    "Найти рабочку по части",
                    "Выход"#Ready
                ]
            },
            4: {
                "flew_row": 1,
                "menu": [
                    "Поиск человека по ФИО",
                    "Выход"#Ready
                ]
            }
            
        }
    
    def message_analys(self, message):
        match(message):

            case "Выход":
                self.set_default()

    def set_default(self):
        self.navIndex = 0

    def navigation(self, message, telebot: TeleBot):
        match message.text:
            #Передвижение по меню
            case "Выписка":
                self.navIndex = 2

            case "Рабочка":
                self.navIndex = 3
            
            case "Поиск по базе":
                self.navIndex = 4
            
            case "Выключение устройства":
                self.navIndex = 1

            #Выключение устройства
            case "Плановое выключение через час":
                os.system("shutdown /s /t 3600")
                telebot.send_message(message.chat.id, "Запланировано выключение через 1 час")
                self.navIndex = 0

            case "Плановое выключение через 20 минут":
                os.system("shutdown /s /t 1200")
                telebot.send_message(message.chat.id, "Запланировано выключение через 20 минут")
                self.navIndex = 0

            case "Отмена выключения":
                os.system("shutdown /a")
                telebot.send_message(message.chat.id, "Запланированное выключение отменено")
                self.navIndex = 0

            #Выписка
            case "Выписка рабочей команды (Плановая)":
                base_manager = DataBaseManager()
                telebot.send_message(message.chat.id, "Подождите секунд 5... Щас сделаю выписку (-_-)!")
                telebot.send_message(message.chat.id, base_manager.select_for_scout_contengent_format_FIO_Date())
                self.navIndex = 0
            
            #Рабочка
            case "Получить файл рабочей команды":
                src = WorkingTeamInformation().file_path_of_working_class
                telebot.send_message(message.chat.id, "Подождите секунд 5... Щас поищу файл рабочки (-_-)!")
                with open(src, 'rb') as excel_file:
                    telebot.send_document(message.chat.id, excel_file)
            
            #Постоянный функционал
            case "Выход":
                self.navIndex = 0

            case _:
                telebot.send_message(message.chat.id, "Указанная вами функция, либо находится в разработке,\nлибо не предусмотрена разработчиком")
                self.navIndex = 0
    
    def defender_menu_manager(self, message, allowed_indexes) -> bool:
        tg_navigation_menu_manager_validator = TGNavifationMenuManagerValidator()


    def chatMenuCreator(self) -> types.ReplyKeyboardMarkup:
        keyboard = types.ReplyKeyboardMarkup(row_width=self.main_menu_content[self.navIndex]["flew_row"])
        for btn in self.main_menu_content[self.navIndex]["menu"]:
            keyboard.add(types.KeyboardButton(btn))
        return keyboard