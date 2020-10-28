from Controllers import DataBaseController as DB
from Controllers import ApiController as API

class MainController():         
    def __init__(self):
        # Instancia a controller que será responsável pelas requests
        self.api = API.ApiController(self)
        self.db = DB.DataBaseController(self)
        self.db.startConnection()
        # Chama a função que armazena os generos de filme no banco
        self.api.getGenres()
        # Chama a função que armazena os filmes no banco (a partir de filmes os outros objetos são armazenados)
        self.api.getTrendingMovies()
        #self.api.getTrendingPeople()

    # Salva no banco um filme específico
    def populateMovie(self, movieJson):
        self.db.saveMovie(movieJson)

    # Salva no banco um filme específico e sua posição no trending
    def populateTrendingMovie(self, position, id, json):
        self.db.saveTrendingMovie(position, id, json)

    # Salva no banco uma pessoa específico e sua posição no trending
    def populateTrendingPerson(self, position, id, json):
        self.db.saveTrendingPerson(position, id, json)

    # Salva no banco os gêneros de um filme
    def populateMovieGenres(self, movieId, genresJson):
        self.db.saveMovieGenres(movieId, genresJson)

    # Salva todos os gêneros no postgresql
    def populateGenres(self, genresJson):
        self.db.saveGenres(genresJson)

    # Salva no banco as companhias de produção
    # e salva os produtores de um filme específico
    def pupulateProductionCompanies(self, movieId, companiesJson):
        self.db.saveProductionCompanies(movieId, companiesJson)

    # Salva no banco os países de produção e gravação
    # e salva os países de produção e gravação de um filme específico
    def pupulateProductionCountries(self, movieId, countriesJson):
        self.db.saveProductionCountries(movieId, countriesJson)

    # Salva no banco uma coleção específica
    def populateCollection(self, collectionJson):
        self.db.saveCollection(collectionJson)

    # Salva no banco um crédito específico
    def populateCredit(self, creditJson, personId, creditId):
        self.db.saveCredit(creditJson, personId, creditId)

    # Salva no banco uma pessoa específica
    def populatePerson(self, personJson):
        self.db.savePerson(personJson)

    # Encerra a conexão com o banco após o uso
    def closeConnection(self):
        self.db.closeConnection()

    # Busca todos os dados de um filme específico a partir do seu id
    def getMovie(self, movieId):
        self.api.getMovie(movieId)

    # Busca todos os dados de uma pessoa específica a partir do seu id
    def getPerson(self, personId):
        self.api.getPerson(personId)

    # Busca todos os dados de uma coleção específica a partir do seu id
    def getCollection(self, collectionId):
        self.api.getCollection(collectionId)

if __name__ == '__main__':
    mainController = MainController()