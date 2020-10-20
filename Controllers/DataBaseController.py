import psycopg2
import time

class DataBaseController(): 
    def __init__(self, mainController):  
        self.mainController = mainController
        # Instancia variáveis da db
        self.dbHost = "localhost"
        self.dbName = "moviedb3"
        self.dbUser = "postgres"
        self.dbPassword = "123456"

    # Inicia a conexão com o postgresql
    def startConnection(self):
        self.connection = psycopg2.connect(host=self.dbHost, database=self.dbName, user=self.dbUser, password=self.dbPassword)
        self.cursor = self.connection.cursor()

    # Encerra a conexão com o postgresql
    def closeConnection(self):
        self.connection = self.connection.close()

    # Salva no postgresql um filme específico
    def saveMovie(self, movieJson):
        originalTitle = str(movieJson["original_title"]).replace("'", " ")
        movieId = str(movieJson["id"])
        originalLanguage = str(movieJson["original_language"])
        popularity = str(movieJson["popularity"])
        status = str(movieJson["status"])
        title = str(movieJson["title"]).replace("'", " ")
        voteAverage = str(movieJson["vote_average"])
        voteCount = str(movieJson["vote_count"])
        releaseDate = str(movieJson["release_date"])
        budget = str(movieJson["budget"])
        revenue = str(movieJson["revenue"])
        runtime = str(movieJson["runtime"])
        if (movieJson["belongs_to_collection"] != None):
            collectionId = str(movieJson["belongs_to_collection"]["id"])
            self.mainController.getCollection(collectionId)
            # É necessário criar a coleção antes, já que se trata de uma fk, então o sleep
            time.sleep(3)
        else:
            collectionId = "null"
        # Monta a query sql
        sql = "insert into movies " + \
            "values (" + movieId + ", '" + originalLanguage + "', '" + originalTitle + "', " + popularity + ", '" + \
            status + "', '" + title + "', " + voteAverage + ", " + voteCount + ", to_date('" + \
            releaseDate + "', 'yyyy-mm-dd'), " + budget + ", " + revenue + ", " + runtime + ", " + collectionId + ")"
        # Executa a query sql no banco
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print("\nFilme " + originalTitle + " salvo com sucesso!")
        except:
            self.connection.rollback()
            pass

    # Salva todos os gêneros no postgresql
    def saveGenres(self, genresJson):
        for genre in genresJson:
            genreId = str(genre["id"])
            genreName = str(genre["name"])
            # Monta a query sql
            sql = "insert into genres values (" + genreId + ", '" + genreName + "')"
            try:
                # Executa a query sql no banco
                self.cursor.execute(sql)
                self.connection.commit()
            except:
                self.connection.rollback()
                pass
        print("\nGêneros salvos com sucesso!")

    # Salva no postgresql uma coleção específica
    def saveCollection(self, collectionJson):
        collectionId = str(collectionJson["id"])
        collectionName = str(collectionJson["name"]).replace("'", "''")
        # Monta a query sql
        sql = "insert into collections values (" + collectionId + ", '" + collectionName + "')"
        # Executa a query sql no banco
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print("\nColeção " + collectionName + " salva com sucesso!")
            # Salva no banco cada filme da coleção
            for part in collectionJson["parts"]:
                self.mainController.getMovie(part["id"])
        except:
            self.connection.rollback()
            pass