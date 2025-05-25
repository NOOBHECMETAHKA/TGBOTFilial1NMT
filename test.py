from Modules.TelegramNavigationMenuManager import TGNavigationMenuManager

menu = TGNavigationMenuManager()
for element in menu.main_menu_content[5]["menu"]:
    print(element)