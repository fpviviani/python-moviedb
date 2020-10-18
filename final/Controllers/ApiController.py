import json, requests

class ApiController(): 
    def __init__(self, mainController):  
        self.mainController = mainController
        self.apiKey = "619e50c9f8b2c6aacab7bbc2db6c67a7"
        self.searchMovie()
        # self.getGenres()

    # Procura por um filme especifico pelo input do usuário
    def searchMovie(self):
        query = str(input('Digite a string pela qual deseja pesquisar: '))
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/search/movie?query="+query+"&api_key="+self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados apenas do primeiro filme encontrado
        results = json.loads(response.content)["results"][0]
        # Consulta os cŕeditos desse filme
        self.getCredits(results.get("id"))
        
    # Busca todos os gêneros cadastrados
    def getGenres(self):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/genre/movie/list?api_key="+self.apiKey+"&language=en-US"
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados dos generos cadastrados
        results = json.loads(response.content)["genres"]
        print (results)

    # Busca os créditos a partir da id de um filme
    def getCredits(self, movieId):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/movie/"+str(movieId)+"/credits?api_key="+self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados dos créditos do filme buscado
        results = json.loads(response.content)["cast"]
        print (results)