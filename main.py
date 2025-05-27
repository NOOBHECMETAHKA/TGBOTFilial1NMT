import telebot
from telebot import types
from Modules.TelegramNavigationMenuManager import TGNavigationMenuManager, TGNavigationMenuManagerValidator

token="7836343375:AAHLiVnEzATa05oW7EDf5tuwaNTKvoKl2eI"
bot=telebot.TeleBot(token)

collectionIDS = [
    1289144600,
    # 7133363448 Саня
]

if __name__ == "__main__":
    menu_manager = TGNavigationMenuManager()
    validator = TGNavigationMenuManagerValidator()

    for id in collectionIDS:
        bot.send_message(id, "Бот запущен")

    # Определяем список команд и их описание
    commands = [
        telebot.types.BotCommand("/start", "Запустить бота"),
        telebot.types.BotCommand("/menu", "Вызвать меню"),
    ]

    # Устанавливаем команды
    bot.set_my_commands(commands)

    @bot.message_handler(commands=['start', "menu"])
    def start_menu(message):
        print(f"Индификатор чата: {message.from_user.id}; Сслыка на пользователя: t.me/{message.from_user.username}")
        if message.chat.id in collectionIDS:
            menu_manager.set_default()
            bot.reply_to(message, "Выбирите функцию на панели!", reply_markup=menu_manager.chatMenuCreator())
        else:
            bot.reply_to(message, "У вас нету прав к функциям бота!")

    
    @bot.message_handler(content_types="text")
    def main_function(message):
        print(f"Индификатор чата: {message.from_user.id}; Сслыка на пользователя: t.me/{message.from_user.username}; Сообщение от пользователя: {message.text}")
        if message.from_user.id in collectionIDS:
            menu_manager.navigation(message=message, telebot=bot)
            if menu_manager.navIndex not in validator.inputer_indexes:
                bot.reply_to(message, "Выбирите функцию на панели!", reply_markup=menu_manager.chatMenuCreator())
        else:
            bot.reply_to(message, "У вас нету прав к функциям бота!")
        
bot.infinity_polling()

