import telebot
from telebot import types
from Modules.TelegramNavigationMenuManager import TGNavigationMenuManager

token="7836343375:AAHLiVnEzATa05oW7EDf5tuwaNTKvoKl2eI"
bot=telebot.TeleBot(token)

collectionIDS = [
    1289144600
]

if __name__ == "__main__":
    menu_manager = TGNavigationMenuManager()

    for id in collectionIDS:
        bot.send_message(id, "Бот запущен")

    # Определяем список команд и их описание
    commands = [
        telebot.types.BotCommand("start", "Запустить бота"),
        telebot.types.BotCommand("/menu", "Вызвать меню"),
    ]

    # Устанавливаем команды
    bot.set_my_commands(commands)

    @bot.message_handler(commands=['start', "menu"])
    def start_menu(message):
        menu_manager.set_default()
        bot.reply_to(message, "Выбирите функцию на панели!", reply_markup=menu_manager.chatMenuCreator())
    
    @bot.message_handler(content_types="text")
    def main_function(message):
        menu_manager.navigation(message=message, telebot=bot)
        bot.reply_to(message, "Выбирите функцию на панели!", reply_markup=menu_manager.chatMenuCreator())

bot.infinity_polling()

