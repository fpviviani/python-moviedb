from Controllers import DataBaseController as DB
from Controllers import ApiController as API

class MainController():         
    def __init__(self):
        # Instancia a controller que será responsável pelas requests
        self.api = API.ApiController(self)
        self.db = DB.DataBaseController(self)
        self.db.startConnection()
        self.api.getGenres()
        # self.api.searchMovie()
        self.api.getTrendingMovies()

    # Salva no postgresql um filme específico
    def populateMovie(self, movieJson):
        self.db.saveMovie(movieJson)

    # Salva todos os gêneros no postgresql
    def populateGenres(self, genresJson):
        self.db.saveGenres(genresJson)

    # Salva no postgresql uma coleção específica
    def populateCollection(self, collectionJson):
        self.db.saveCollection(collectionJson)

    # Encerra a conexão com o banco após o uso
    def closeConnection(self):
        self.db.closeConnection()

    # Busca todos os dados de um filme específico a partir do seu id
    def getMovie(self, movieId):
        self.api.getMovie(movieId)

    # Busca todos os dados de uma coleção específica a partir do seu id
    def getCollection(self, collectionId):
        self.api.getCollection(collectionId)

if __name__ == '__main__':
    mainController = MainController()