from Controllers import DataBaseController as DB
from Controllers import ApiController as API
import tkinter as tk
from Views import MainView as MV

class MainController():         
    def __init__(self):
        # Instancia a controller que será responsável pelas requests
        self.api = API.ApiController(self)
        self.db = DB.DataBaseController(self)
        self.db.startConnection()
        # Chama a função que armazena os generos de filme no banco
        self.api.getGenres()
        # Instancia a view principal
        self.mainTk = tk.Tk()
        self.mainTk.resizable(width=False, height=False)
        self.mv = MV.MainView(self.mainTk, self) 
        self.mainTk.mainloop()

    # Salva no banco um filme específico
    def populateMovie(self, movieJson):
        self.db.saveMovie(movieJson)

    # Salva no banco um filme específico e sua posição no trending
    def populateTrendingMovie(self, position, id, json):
        self.db.saveTrendingMovie(position, id, json)

    # Busca os filmes que estão no trending
    def getTrendingMovie(self):
        self.api.getTrendingMovies()

    # Salva no banco uma pessoa específico e sua posição no trending
    def populateTrendingPerson(self, position, id, json):
        self.db.saveTrendingPerson(position, id, json)

    # Salva no banco os gêneros de um filme
    def populateMovieGenres(self, movieId, genresJson):
        self.db.saveMovieGenres(movieId, genresJson)

    # Busca as pessoas que estão no trending
    def getTrendingPeople(self):
        self.api.getTrendingPeople()

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

    # Encerra a conexão com o banco após o uso.
    def closeConnection(self):
        self.db.closeConnection()

    # Busca todos os dados de um filme específico a partir do seu id
    def getMovie(self, movieId):
        self.api.getMovie(movieId)

    # Busca todos os dados de uma pessoa específica a partir do seu id
    def getPerson(self, personId):
        self.api.getPerson(personId)

    # Busca todos os dados de uma pessoa específica a partir do seu nome
    def searchPerson(self, personName):
        self.api.searchPerson(personName)

    # Busca todos os dados de um filme específico a partir do seu nome
    def searchMovie(self, movieName):
        self.api.searchMovie(movieName)

    # Busca todos os dados de uma coleção específica a partir do seu id
    def getCollection(self, collectionId):
        self.api.getCollection(collectionId)

    # Exibe uma string de resposta no console da view
    def outputResponse(self, responseString):
        self.mv.serverResponse(responseString)

if __name__ == '__main__':
    mainController = MainController()