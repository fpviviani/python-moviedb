import json, requests

class ApiController(): 
    def __init__(self, mainController):  
        self.mainController = mainController
        self.apiKey = "619e50c9f8b2c6aacab7bbc2db6c67a7"
        self.searchMovie()
        self.getGenres()

    def searchMovie(self):
        query = str(input('Digite a string pela qual deseja pesquisar: '))
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/search/movie?query="+query+"&api_key="+self.apiKey
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados apenas do primeiro filme encontrado
        results = json.loads(response.content)["results"][0]
        # print (results)
        
    def getGenres(self):
        # Monta a url da request que será feita
        requestUrl = "https://api.themoviedb.org/3/genre/movie/list?api_key="+self.apiKey+"&language=en-US"
        # Pega o conteudo da resposta
        response = requests.get(requestUrl)
        # Separa os dados apenas do primeiro filme encontrado
        results = json.loads(response.content)["genres"]
        print (results)