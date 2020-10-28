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
        movieId = str(movieJson["id"])
        originalTitle = str(movieJson["original_title"]).replace("'", " ")
        originalLanguage = str(movieJson["original_language"]).replace("'", " ")
        popularity = str(movieJson["popularity"])
        status = str(movieJson["status"])
        title = str(movieJson["title"]).replace("'", " ")
        voteAverage = str(movieJson["vote_average"])
        voteCount = str(movieJson["vote_count"])
        budget = str(movieJson["budget"])
        revenue = str(movieJson["revenue"])
        runtime = str(movieJson["runtime"])
        # print(movieJson)
        if (movieJson["belongs_to_collection"] != "null"):
            collectionId = str(movieJson["belongs_to_collection"]["id"])
            self.mainController.getCollection(collectionId)
            # É necessário criar a coleção antes, já que se trata de uma fk, então o sleep
            time.sleep(3)
        else:
            collectionId = "null"

        # Monta a query sql
        sql = "insert into movies " + \
              "values (" + movieId + ", '" + originalLanguage + "', '" + originalTitle + "', " + popularity + ", '" + \
              status + "', '" + title + "', " + voteAverage + ", " + voteCount + ", "

        releaseDate = str(movieJson["release_date"])
        if (releaseDate != "null"):
            sql += "to_date('" + releaseDate + "', 'yyyy-mm-dd'), " + budget + ", " + revenue + ", " + runtime + ", " + collectionId + ")"
        else:
            sql += releaseDate + ", " + budget + ", " + revenue + ", " + runtime + ", " + collectionId + ")"
        # Executa a query sql no banco
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print("\nFilme " + title + " salvo com sucesso!")
            # Salva no banco cada gênero do filme
            self.mainController.populateMovieGenres(movieId, movieJson["genres"])
            # Salva no banco cada companhia de produção do filme
            self.mainController.pupulateProductionCompanies(movieId, movieJson["production_companies"])
            # Salva no banco cada país de produção do filme
            self.mainController.pupulateProductionCountries(movieId, movieJson["production_countries"])
        except:
            self.connection.rollback()
            pass

    # Salva no postgresql um trending específico
    def saveTrendingMovie(self, position, id):
        try:
            # Monta a query sql
            sql = "insert into trending_movie values (" + str(position) + str(id) +")"
        # Executa a query sql no banco
            self.cursor.execute(sql)
            self.connection.commit()
            print("\Trending " + position + " salvo com sucesso!")
        except:
            self.connection.rollback()
            # Monta a query sql
            sql = "update trending_movie set movie_id = " + str(id) +" where id = "+ position 
            try:
                # Executa a query sql no banco
                self.cursor.execute(sql)
                self.connection.commit()
                print("\Trending " + position + " atualizado com sucesso!")
            except:
                self.connection.rollback()
                pass

    # Salva no postgresql um trending específico
    def saveTrendingPerson(self, position, id):
        try:
            # Monta a query sql
            sql = "insert into trending_person values (" + str(position) + str(id) +")"
        # Executa a query sql no banco
            self.cursor.execute(sql)
            self.connection.commit()
            print("\Trending " + position + " salvo com sucesso!")
        except:
            self.connection.rollback()
            # Monta a query sql
            sql = "update trending_person set person_id = " + str(id) +" where id = "+ position 
            try:
                # Executa a query sql no banco
                self.cursor.execute(sql)
                self.connection.commit()
                print("\Trending " + position + " atualizado com sucesso!")
            except:
                self.connection.rollback()
                pass

    # Salva todos os gêneros de um filme no postgresql
    def saveMovieGenres(self, movieId, genresJson):
        for genre in genresJson:
            genreId = str(genre["id"])
            # Monta a query sql
            sql = "insert into movie_genres values (" + movieId + ", " + genreId + ")"
            try:
                # Executa a query sql no banco
                self.cursor.execute(sql)
                self.connection.commit()
            except:
                self.connection.rollback()
                pass
        print("\nGênero(s) do filme salvo(s) com sucesso!")

    # Salva todos os gêneros no postgresql
    def saveGenres(self, genresJson):
        for genre in genresJson:
            genreId = str(genre["id"])
            genreName = str(genre["name"]).replace("'", " ")
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

    # Salva no postgresql as companhias de produção
    def saveProductionCompanies(self, movieId, companiesJson):
        for company in companiesJson:
            companyId = str(company["id"])
            companyName = str(company["name"]).replace("'", " ")
            companyOriginCountry = str(company["origin_country"]).replace("'", " ")
            # Monta a query sql
            # Salvar a companhia de produção
            sql = "insert into production_companies values (" + companyId + ", '" + companyName + "', '" + companyOriginCountry + "')"
            try:
                # Executa a query sql no banco
                self.cursor.execute(sql)
                self.connection.commit()
            except:
                self.connection.rollback()
                pass

            # Salvar a companhia de produção do filme específico
            sql2 = "insert into movie_production_companies values (" + movieId + ", " + companyId + ")"
            try:
                # Executa a query sql no banco
                self.cursor.execute(sql2)
                self.connection.commit()
            except:
                self.connection.rollback()
                pass
        print("\nCompanhia(s) de Produção do filme salva(s) com sucesso!")

    # Salva no postgresql os países de produção do filme
    def saveProductionCountries(self, movieId, countriesJson):
        for country in countriesJson:
            countryId = str(country["iso_3166_1"])
            countryName = str(country["name"]).replace("'", " ")
            # Monta a query sql
            # Salvar o país de produção
            sql = "insert into production_countries values ('" + countryId + "', '" + countryName + "')"
            try:
                # Executa a query sql no banco
                self.cursor.execute(sql)
                self.connection.commit()
            except:
                self.connection.rollback()
                pass

            # Salvar o país de produção do filme específico
            sql2 = "insert into movie_production_countries values (" + movieId + ", '" + countryId + "')"
            try:
                # Executa a query sql no banco
                self.cursor.execute(sql2)
                self.connection.commit()
            except:
                self.connection.rollback()
                pass
        print("\nPaís(es) de Produção do filme salvo(s) com sucesso!")

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

    # Salva no postgresql um crédito específico
    def saveCredit(self, creditJson, personId, creditId):
        self.mainController.getPerson(personId)
        time.sleep(3)
        creditType = str(creditJson["credit_type"]).replace("'", "''")
        creditDepartment = str(creditJson["department"]).replace("'", "''")
        creditJob = str(creditJson["job"]).replace("'", "''")
        if(creditType != "crew"):
            creditCharacter = str(creditJson["media"]["character"]).replace("'", "''")
        else:
            creditCharacter = "null"
        movieId = str(creditJson["id"])

        # Monta a query sql
        sql = "insert into credits values (" + str(creditId) + ", '" + creditType + "', '" + creditDepartment + "', '" + creditJob + \
            "', '" + creditCharacter + "', " + movieId + ", " + str(personId) + ")"
        # Executa a query sql no banco
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print("\nCrédito " + creditId + " salvo com sucesso!")
        except:
            self.connection.rollback()
            pass

    # Salva no postgresql uma pessoa específica
    def savePerson(self, personJson):
        personId = str(personJson["id"])
        name = str(personJson["name"]).replace("'", " ")
        gender = str(personJson["gender"])
        popularity = str(personJson["popularity"])
        place_of_birth = str(personJson["place_of_birth"]).replace("'", " ")
        known_for_department = str(personJson["known_for_department"]).replace("'", " ")
        # Monta a query sql
        sql = "insert into people " + \
              "values (" + personId + ", '" + name + "', " + gender + ", " + popularity + ", '" + \
              place_of_birth + "', "
        birthday = str(personJson["birthday"])
        if (birthday != "null"):
            sql += "to_date('" + birthday + "', 'yyyy-mm-dd'), "
        else:
            sql += birthday + ", "
        deathday = str(personJson["deathday"])
        if (deathday != "null"):
            sql += "to_date('" + deathday + "', 'yyyy-mm-dd'), '" + known_for_department + "')"
        else:
            sql += deathday + ", '" + known_for_department + "')"
        # Executa a query sql no banco
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print("\nPessoa: " + name + " salva com sucesso!")
        except:
            self.connection.rollback()
            pass