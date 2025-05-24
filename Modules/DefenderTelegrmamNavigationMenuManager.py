from Modules.TelegramNavigationMenuManager import TGNavigationMenuManager

class TGNavigationMenuManagerValidator:
    def __init__(self, chValidator=True):
        self.indexes_routes = [0, 1, 2, 3, 4]
        self.routes = self.available_routes()
        self.chValidator = chValidator
        self.message = str
    
    def available_routes() -> list:
        router = list()
        navigator = TGNavigationMenuManager()
        for indexer_rout in navigator.main_menu_content:
            for route_name in navigator.main_menu_content[indexer_rout]["menu"]:
                router.append(route_name)
        return router

    def set_error(self, message: str):
        if message != "":
            self.chValidator = False
            self.message = message

    def get_error(self) -> str:
        return self.message