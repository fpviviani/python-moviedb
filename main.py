from Controllers import DataBaseController as DB
from Controllers import ApiController as API

class MainController():         
    def __init__(self):
        # Instancia a controller que será responsável pelas requests
        self.api = API.ApiController(self)

if __name__ == '__main__':
    mainController = MainController()