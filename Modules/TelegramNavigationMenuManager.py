import os 
from telebot import types, TeleBot
from Modules.DataBaseManager import DataBaseManager
from Modules.WorkingTeamInformationCollection import WorkingTeamInformation

class TGNavigationMenuManagerValidator():
    def __init__(self):
        self.inputer_indexes = [98, 99]
    
    def available_routes(self) -> list:
        router = list()
        navigator = TGNavigationMenuManager()
        for indexer_rout in navigator.main_menu_content:
            for route_name in navigator.main_menu_content[indexer_rout]["menu"]:
                router.append(route_name)
        return router

class TGNavigationMenuManager():
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
                    "Отключение бота", #Ready
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
                    "Получить файл рабочей команды",#Ready
                    "Получить список для построяния",
                    "Найти рабочку по ФИО",#Ready
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
            },
            5: {
                "flew_row": 5,
                "menu": {
                    "1/2":[1, 2],
                    "3":[3],
                    "4/5":[4, 5],
                    "6/7":[6, 7],
                    "10/11":[10, 11],
                    "16/36":[16, 36],
                    "17":[17],
                    "18":[18],
                    "19":[19],
                    "21":[21],
                    "24/25/26":[24, 25, 26],
                    "32":[32],
                    "33":[33]
                }
            }
        }

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

            case "Отключение бота":
                telebot.send_message(message.chat.id, "Отключаюсь!")
                telebot.stop_polling()
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

            case "Выписка части (Плановая)":
                self.navIndex = 98
                working_team_manager = WorkingTeamInformation()
                base_manager = DataBaseManager()
                telebot.send_message(message.chat.id, "Введите номер части для формирования выписки:")
            
            #Рабочка
            case "Получить файл рабочей команды":
                src = WorkingTeamInformation().file_path_of_working_class
                telebot.send_message(message.chat.id, "Подождите секунд 5... Щас поищу файл рабочки (-_-)!")
                with open(src, 'rb') as excel_file:
                    telebot.send_document(message.chat.id, excel_file)
                self.navIndex = 0
            
            case "Найти рабочку по ФИО":
                self.navIndex = 99
                telebot.send_message(message.chat.id, "Введите примерный отрезок ФИО:")

            #Постоянный функционал
            case "Выход":
                self.navIndex = 0

            case _:
                validator = TGNavigationMenuManagerValidator()
                if self.navIndex in validator.inputer_indexes:
                    match self.navIndex:
                        case 98:
                            base_manager = DataBaseManager("TEST", "TEST")
                            telebot.send_message(message.chat.id, "Подождите секунд 5... Щас сделаю выписку (-_-)!")
                            telebot.send_message(message.chat.id, base_manager.select_oct_contengent_for_military_unit(message.text))
                            self.navIndex = 0
                        case 99:
                            working_team_manager = WorkingTeamInformation()
                            telebot.send_message(message.chat.id, working_team_manager.find_working_man_from_working_team_by_fullname_text_card(message.text))
                            self.navIndex = 0
                        case _:
                            telebot.send_message(message.chat.id, "Указанная вами принимающая функция не найдена!")
                            self.navIndex = 0
                else:          
                    telebot.send_message(message.chat.id, "Указанная вами функция не найдена!")
                    self.navIndex = 0

    #Создаёт меню исходя из указателя
    def chatMenuCreator(self) -> types.ReplyKeyboardMarkup:
        '''
        Получается индекс и исходя из него получает необходимое меню
        '''
        keyboard = types.ReplyKeyboardMarkup(row_width=self.main_menu_content[self.navIndex]["flew_row"])
        for btn in self.main_menu_content[self.navIndex]["menu"]:
            keyboard.add(types.KeyboardButton(btn))
        return keyboard
    
    def chatMenuCreatorByIndex(self, index: int) -> types.ReplyKeyboardMarkup:
        '''
        Получается индекс и исходя из него получает необходимое меню
        '''
        keyboard = types.ReplyKeyboardMarkup(row_width=self.main_menu_content[index]["flew_row"])
        for btn in self.main_menu_content[self.navIndex]["menu"]:
            keyboard.add(types.KeyboardButton(btn))
        return keyboard
        
