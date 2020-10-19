import json, requests

class ApiController(): 
    def __init__(self, mainController):  
        self.mainController = mainController
        self.apiKey = "619e50c9f8b2c6aacab7bbc2db6c67a7"
        self.searchMovie()
        # self.getGenres()
        # self.searchPerson()

    # Procura por um filme especifico pelo input do usuário
    def searchMovie(self):
        query = str(input('Digite o filme pelo qual deseja pesquisar: '))
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/search/movie?query="+query+"&api_key="+self.apiKey
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
        requestUrl = "https://api.themoviedb.org/3/movie/"+str(movieId)+"?api_key=" + self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados do filme
        results = json.loads(response.content)
        if (results["belongs_to_collection"]["id"]):
            collectionId = results["belongs_to_collection"]["id"]
            self.getCollection(collectionId)

        # print("Dados do filme")
        # print(results)

    # Busca todos os gêneros cadastrados
    def getGenres(self):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/genre/movie/list?api_key="+self.apiKey+"&language=en-US"
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados dos generos cadastrados
        results = json.loads(response.content)["genres"]
        # print("Gêneros de filme")
        # print (results)

    # Busca os créditos a partir do id de um filme
    def getCredits(self, movieId):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/movie/"+str(movieId)+"/credits?api_key="+self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados dos créditos do filme buscado
        results = json.loads(response.content)["cast"]
        # print("Créditos do filme")
        # print (results)

    # Procura por uma pessoa especifica pelo input do usuário
    def searchPerson(self):
        query = str(input('Digite a pessoa pela qual deseja pesquisar: '))
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/search/person?query="+query+"&api_key="+self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados apenas da primeira pessoa encontrada
        results = json.loads(response.content)["results"][0]
        # Consulta os dados da pessoa
        self.getPerson(results.get("id"))

    # Busca todos os dados de uma pessoa específica a partir do seu id
    def getPerson(self, personId):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/person/"+str(personId)+"?api_key=" + self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados da pessoa
        results = json.loads(response.content)
        # print("Dados da pessoa")
        # print(results)

    # Busca todos os dados de uma coelção específica a partir do seu id
    def getCollection(self, collectionId):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/collection/"+str(collectionId)+"?api_key=" + self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados da pessoa
        results = json.loads(response.content)
        print("Dados da coleção")
        print(results)