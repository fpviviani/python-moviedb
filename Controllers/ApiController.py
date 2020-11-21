import json, requests


class ApiController():
    def __init__(self, mainController):
        self.mainController = mainController
        self.apiKey = "619e50c9f8b2c6aacab7bbc2db6c67a7"

    # Procura por um filme especifico pelo input do usuário
    def searchMovie(self, movieName):
        query = str(movieName)
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/search/movie?query=" + query + "&api_key=" + self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados apenas do primeiro filme encontrado
        results = json.loads(response.content)["results"][0]
        # Consulta os dados do filme
        self.getMovie(results.get("id"))
        # Consulta os cŕeditos desse filme
        self.getCredits(results.get("id"))

    # Busca todos os dados de um filme específico a partir do seu id
    def getMovie(self, movieId):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/movie/" + str(movieId) + "?api_key=" + self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados do filme
        results = json.loads(response.content)
        # Checa se a request deu certo
        results = self.verifyRequest(response, results)
        if (results != False):
            # Envia o resultado pra controller principal
            self.mainController.populateMovie(results)
            self.getCredits(movieId)

    # Busca todos os gêneros cadastrados
    def getGenres(self):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/genre/movie/list?api_key=" + self.apiKey + "&language=en-US"
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados dos generos cadastrados
        results = json.loads(response.content)["genres"]
        # Checa se a request deu certo
        results = self.verifyRequest(response, results)
        if (results != False):
            # Envia o resultado pra controller principal
            self.mainController.populateGenres(results)

    # Busca os créditos a partir do id de um filme
    def getCredits(self, movieId):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/movie/" + str(movieId) + "/credits?api_key=" + self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados dos créditos do filme buscado
        results = json.loads(response.content)["cast"]
        # Checa se a request deu certo
        results = self.verifyRequest(response, results)
        if (results != False):
            # Percorre cada crédito do filme obtendo mais detalhes sobre o mesmo
            x = 0
            for credit in results:
                x += 1
                self.getCreditDetails(credit["credit_id"], credit["id"])
                if (x == 10):
                    break

    # Busca os detalhes de um crédito específico a partir de sua id
    def getCreditDetails(self, creditId, personId):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/credit/" + str(creditId) + "?api_key=" + self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados dos créditos do filme buscado
        results = json.loads(response.content)
        # Checa se a request deu certo
        results = self.verifyRequest(response, results)
        if (results != False):
            # Envia o resultado pra controller principal
            self.mainController.populateCredit(results, personId, creditId)

    # Procura por uma pessoa especifica pelo input do usuário
    def searchPerson(self, personName):
        query = str(personName)
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/search/person?query=" + query + "&api_key=" + self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados apenas da primeira pessoa encontrada
        results = json.loads(response.content)["results"][0]
        # Checa se a request deu certo
        results = self.verifyRequest(response, results)
        if (results != False):
            # Consulta os dados da pessoa
            self.getPerson(results.get("id"))

    # Busca todos os dados de uma pessoa específica a partir do seu id
    def getPerson(self, personId):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/person/" + str(personId) + "?api_key=" + self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados da pessoa
        results = json.loads(response.content)
        # Checa se a request deu certo
        results = self.verifyRequest(response, results)
        if (results != False):
            # Envia o resultado pra controller principal
            self.mainController.populatePerson(results)

    # Busca todos os dados de uma coleção específica a partir do seu id
    def getCollection(self, collectionId):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/collection/" + str(collectionId) + "?api_key=" + self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados da coleção
        results = json.loads(response.content)
        # Checa se a request deu certo
        results = self.verifyRequest(response, results)
        if (results != False):
            # Envia o resultado pra controller principal
            self.mainController.populateCollection(results)

    # Busca os filmes que estão no trending
    def getTrendingMovies(self):
        aux = 1
        # Percorre as 34 primeiras páginas dos trendings
        # range(1, 11)
        for page in range(1, 35):
            # Monta a url da request que será feita
            requestUrl = "https://api.themoviedb.org/3/trending/movie/day?api_key=" + self.apiKey + "&page=" + str(page)
            # Pega o conteudo da resposta
            response = requests.get(requestUrl)
            # Separa os filmes que estão no trending
            results = json.loads(response.content)["results"]
            # Checa se a request deu certo
            results = self.verifyRequest(response, results)
            if(results != False):
                # Percorre cada filme do trending e salva no banco
                for movie in results:
                    #self.getMovie(movie["id"])
                    self.mainController.populateTrendingMovie(aux, movie["id"], movie)
                    aux = aux + 1
            
    # Busca as pessoas que estão no trending
    def getTrendingPeople(self):
        aux = 1
        # Percorre as 34 primeiras páginas dos trendings
        for page in range(1, 35):
            # Monta a url da request que será feita
            requestUrl = "https://api.themoviedb.org/3/trending/person/day?api_key=" + self.apiKey + "&page=" + str(
                page)
            # Pega o conteudo da resposta
            response = requests.get(requestUrl)
            # Separa as pessoas que estão no trending
            results = json.loads(response.content)["results"]
            # Checa se a request deu certo
            results = self.verifyRequest(response, results)
            if (results != False):
                # Percorre cada pessoa do trending e salva no banco
                for person in results:
                    self.getPerson(person["id"])
                    self.mainController.populateTrendingPerson(aux, person["id"], person)
                    aux = aux + 1

    # Verifica se a request foi bem sucedida
    def verifyRequest(self, response, results):
        # Se o código de status da request não for o código positivo, retorna falso
        if (response.status_code != 200):
            return False
        results = self.verifyNone(results)
        return results

    # Verifica se dentre as informações retornadas, alguma se encontra vazia
    def verifyNone(self, results):
        for result in results:
            if (type(result) is dict):
                for key in result:
                    if (result[key] is None):
                        result[key] = "null"
            else:
                if (results[result] is None):
                    results[result] = "null"
        return results
