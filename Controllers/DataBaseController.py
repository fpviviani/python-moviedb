import psycopg2
import time
from datetime import datetime
from pymongo import MongoClient

class DataBaseController(): 
    def __init__(self, mainController):  
        self.mainController = mainController
        # Instancia variáveis da db (Postgresql)
        self.dbHost = "localhost"
        self.dbName = "moviedb"
        self.dbUser = "postgres"
        self.dbPassword = "postgres"

        # Instancia variáveis da db (MongoDB)
        self.client = MongoClient("localhost", 27017)
        self.mongo = self.client.moviedb

    # Inicia a conexão com o banco
    def startConnection(self):
        self.connection = psycopg2.connect(host=self.dbHost, database=self.dbName, user=self.dbUser, password=self.dbPassword)
        self.cursor = self.connection.cursor()

    # Encerra a conexão com o banco
    def closeConnection(self):
        self.connection = self.connection.close()

    # Salva no banco um filme específico
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
        if (movieJson["belongs_to_collection"] != "null"):
            collectionId = str(movieJson["belongs_to_collection"]["id"])
            collectionId2 = str(movieJson["belongs_to_collection"]["id"])
            self.mainController.getCollection(collectionId)
            # É necessário criar a coleção antes, já que se trata de uma fk, então o sleep
            time.sleep(3)
        else:
            collectionId = "null"
            collectionId2 = None

        # Monta a query sql
        sql = "insert into movies " + \
              "values (" + movieId + ", '" + originalLanguage + "', '" + originalTitle + "', " + popularity + ", '" + \
              status + "', '" + title + "', " + voteAverage + ", " + voteCount + ", "

        releaseDate = str(movieJson["release_date"])
        if (releaseDate != "null"):
            sql += "to_date('" + releaseDate + "', 'yyyy-mm-dd'), " + budget + ", " + revenue + ", " + runtime + ", " + collectionId + ")"
        else:
            sql += releaseDate + ", " + budget + ", " + revenue + ", " + runtime + ", " + collectionId + ")"
            releaseDate = None
        # Executa a query sql no banco
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            responseString = "Filme " + title + " salvo com sucesso!"
            self.mainController.outputResponse(responseString)
            # Salva no banco cada gênero do filme
            self.mainController.populateMovieGenres(movieId, movieJson["genres"])
            # Salva no banco cada companhia de produção do filme
            self.mainController.pupulateProductionCompanies(movieId, movieJson["production_companies"])
            # Salva no banco cada país de produção do filme
            self.mainController.pupulateProductionCountries(movieId, movieJson["production_countries"])
        except:
            self.connection.rollback()
            pass
        # Monta o JSON
        movie = {
            "_id": movieJson["id"],
            "belongs_to_collection": collectionId2,
            "original_language": movieJson["original_language"],
            "original_title": movieJson["original_title"],
            "title": movieJson["title"],
            "popularity": movieJson["popularity"],
            "status": movieJson["status"],
            "vote_average": movieJson["vote_average"],
            "vote_count": movieJson["vote_count"],
            "genres": movieJson["genres"],
            "release_date": releaseDate,
            "budget": movieJson["budget"],
            "revenue": movieJson["revenue"],
            "runtime": movieJson["runtime"],
            "production_companies": movieJson["production_companies"],
            "production_countries": movieJson["production_countries"]
        }
        try:
            # Faz a inserção do JSON no mongo
            self.mongo.movies.insert_one(movie)
        except:
            pass

    # Salva no banco um trending específico
    def saveTrendingMovie(self, position, id, json):
        try:
            # Monta a query sql
            sql = "insert into trending_movies values (" + str(position) + ",'" + datetime.today().strftime('%Y-%m-%d') + \
                  "'," + str(id) +")"
            # Executa a query sql no banco
            self.cursor.execute(sql)
            self.connection.commit()
            responseString = "Trending " + str(position) + " salvo com sucesso!"
            self.mainController.outputResponse(responseString)
        except:
            self.connection.rollback()
            # Monta a query sql
            sql = "update trending_movies set id_movie = " + str(id) +", trend_date = '" + datetime.today().strftime('%Y-%m-%d') \
                  + "' where trend_id = "+ str(position)
            try:
                # Executa a query sql no banco
                self.cursor.execute(sql)
                self.connection.commit()
                responseString = "Trending " + str(position) + " atualizado com sucesso!"
                self.mainController.outputResponse(responseString)
            except:
                self.connection.rollback()
                pass
        try:
            # Monta o JSON
            data = str(datetime.today().strftime('%Y-%m-%d'))
            trend = {
                "_id": position,
                "movie": {
                    "id": id,
                    "title": json["title"],
                    "release_date": json["release_date"],
                    "original_language": json["original_language"],
                    "original_title": json["original_title"],
                    "genre_ids": json["genre_ids"],
                    "popularity": json["popularity"]
                },
                "trend_date": data
            }
            # Faz a inserção do JSON no mongo
            self.mongo.trending_movies.insert_one(trend)
        except:
            try:
                # Monta o JSON
                data = str(datetime.today().strftime('%Y-%m-%d'))
                trend = {
                    "_id": position,
                    "movie": {
                        "id": id,
                        "title": json["title"],
                        "release_date": json["release_date"],
                        "original_language": json["original_language"],
                        "original_title": json["original_title"],
                        "genre_ids": json["genre_ids"],
                        "popularity": json["popularity"]
                    },
                    "trend_date": data
                }
                # Faz a inserção do JSON no mongo
                myquery = {"_id": position}
                newvalues = {"$set": {"movie": {"id": id, "title": json["title"], "release_date": json["release_date"],
                            "original_language": json["original_language"], "original_title": json["original_title"],
                            "genre_ids": json["genre_ids"], "popularity": json["popularity"]}, "trend_date": data}}
                self.mongo.trending_movies.update_one(myquery, newvalues)
            except:
                pass

    # Salva no banco um trending específico
    def saveTrendingPerson(self, position, id, json):
        try:
            # Monta a query sql
            sql = "insert into trending_people values (" + str(position) + ",'" + datetime.today().strftime('%Y-%m-%d') \
                  + "'," + str(id) +")"
            # Executa a query sql no banco
            self.cursor.execute(sql)
            self.connection.commit()
            responseString = "Trending " + str(position) + " salvo com sucesso!"
            self.mainController.outputResponse(responseString)
        except:
            self.connection.rollback()
            # Monta a query sql
            sql = "update trending_people set id_people = " + str(id) + ", trend_date = '" + datetime.today().strftime('%Y-%m-%d') \
                  + "' where trend_id = "+ str(position)
            try:
                # Executa a query sql no banco
                self.cursor.execute(sql)
                self.connection.commit()
                responseString = "Trending " + str(position) + " atualizado com sucesso!"
                self.mainController.outputResponse(responseString)
            except:
                self.connection.rollback()
                pass
        try:
            # Monta o JSON
            data = str(datetime.today().strftime('%Y-%m-%d'))
            trend = {
                "_id": position,
                "person": {
                    "id": id,
                    "name": json["name"],
                    "known_for_department": json["known_for_department"],
                    "popularity": json["popularity"]
                },
                "trend_date": data
            }
            # Faz a inserção do JSON no mongo
            self.mongo.trending_people.insert_one(trend)
        except:
            try:
                # Monta o JSON
                data = str(datetime.today().strftime('%Y-%m-%d'))
                trend = {
                    "_id": position,
                    "person": {
                        "id": id,
                        "name": json["name"],
                        "known_for_department": json["known_for_department"],
                        "popularity": json["popularity"]
                    },
                    "trend_date": data
                }
                # Faz a inserção do JSON no mongo
                myquery = {"_id": position}
                newvalues = {"$set": {"person": {"id": id, "name": json["name"], "known_for_department": json["known_for_department"],
                                                  "popularity": json["popularity"]}, "trend_date": data}}
                self.mongo.trending_people.update_one(myquery, newvalues)
            except:
                pass

    # Salva todos os gêneros de um filme no banco
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
        responseString = "Gênero(s) do filme salvo(s) com sucesso!"
        self.mainController.outputResponse(responseString)

    # Salva todos os gêneros no banco
    def saveGenres(self, genresJson):
        for genre in genresJson:
            genreId = str(genre["id"])
            genreName = str(genre["name"]).replace("'", " ")
            # Monta a query sql
            sql = "insert into genres values (" + genreId + ", '" + genreName + "')"
            # Monta o JSON
            genre = {
                "_id": genre["id"],
                "name": genreName
            }
            try:
                # Executa a query sql no postgres
                self.cursor.execute(sql)
                self.connection.commit()
            except:
                self.connection.rollback()
                pass
            try:
                # Faz a inserção do JSON no mongo
                self.mongo.genres.insert_one(genre)
            except:
                pass
        responseString = "Gêneros salvos com sucesso!"
        self.mainController.outputResponse(responseString)
        
    # Salva no banco as companhias de produção
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
        responseString = "Companhia(s) de Produção do filme salva(s) com sucesso!"
        self.mainController.outputResponse(responseString)

    # Salva no banco os países de produção do filme
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
        responseString = "País(es) de Produção do filme salvo(s) com sucesso!"
        self.mainController.outputResponse(responseString)

    # Salva no banco uma coleção específica
    def saveCollection(self, collectionJson):
        collectionId = str(collectionJson["id"])
        collectionName = str(collectionJson["name"]).replace("'", "''")
        # Monta a query sql
        sql = "insert into collections values (" + collectionId + ", '" + collectionName + "')"
        # Executa a query sql no banco
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            responseString = "Coleção " + collectionName + " salva com sucesso!"
            self.mainController.outputResponse(responseString)
            # Salva no banco cada filme da coleção
            for part in collectionJson["parts"]:
                self.mainController.getMovie(part["id"])
        except:
            self.connection.rollback()
            pass
        colecao = []
        for i in collectionJson["parts"]:
            if (i.get("release_date")):
                release = i["release_date"]
            else:
                release = None
            aux = {
                "id": i["id"],
                "title": i["title"],
                "release_date": release,
                "original_language": i["original_language"],
                "original_title": i["original_title"],
                "genre_ids": i["genre_ids"],
                "popularity": i["popularity"]
            }
            colecao.append(aux)
        # Monta o JSON
        collection = {
            "_id": collectionJson["id"],
            "name": collectionName,
            "parts": colecao
        }
        try:
            # Faz a inserção do JSON no mongo
            self.mongo.collections.insert_one(collection)
        except:
            pass

    # Salva no banco um crédito específico
    def saveCredit(self, creditJson, personId, creditId):
        self.mainController.getPerson(personId)
        time.sleep(1)
        creditType = str(creditJson["credit_type"]).replace("'", "''")
        creditDepartment = str(creditJson["department"]).replace("'", "''")
        creditJob = str(creditJson["job"]).replace("'", "''")
        if (creditType != "crew"):
            creditCharacter = str(creditJson["media"]["character"]).replace("'", "''")
            creditCharacter2 = str(creditJson["media"]["character"]).replace("'", "''")
        else:
            creditCharacter = "null"
            creditCharacter2 = None
        movieId = str(creditJson["media"]["id"])

        # Monta a query sql
        sql = "insert into credits values ('" + str(
            creditId) + "', '" + creditType + "', '" + creditDepartment + "', '" + creditJob + \
              "', '" + creditCharacter + "', " + movieId + ", " + str(personId) + ")"
        # Monta o JSON
        if (creditJson["person"].get("popularity")):
            popularity = creditJson["person"]["popularity"]
        else:
            popularity = None
        credit = {
            "_id": creditId,
            "credit_type": creditType,
            "department": creditDepartment,
            "job": creditJob,
            "media": {
                "id": creditJson["media"]["id"],
                "vote_count": creditJson["media"]["vote_count"],
                "vote_average": creditJson["media"]["vote_average"],
                "title": creditJson["media"]["title"],
                "release_date": creditJson["media"]["release_date"],
                "original_language": creditJson["media"]["original_language"],
                "original_title": creditJson["media"]["original_title"],
                "genre_ids": creditJson["media"]["genre_ids"],
                "popularity": creditJson["media"]["popularity"],
                "character": creditCharacter2
            },
            "person": {
                "id": personId,
                "name": creditJson["person"]["name"],
                "gender": creditJson["person"]["gender"],
                "known_for_department": creditJson["person"]["known_for_department"],
                "popularity": popularity
            }
        }
        # Executa a query sql no banco
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            responseString = "Crédito " + str(creditId) + " salvo com sucesso!"
            self.mainController.outputResponse(responseString)
        except:
            self.connection.rollback()
            pass
        try:
            # Faz a inserção do JSON no mongo
            self.mongo.credits.insert_one(credit)
        except:
            pass

    # Salva no banco uma pessoa específica
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
            birthday = None
        deathday = str(personJson["deathday"])
        if (deathday != "null"):
            sql += "to_date('" + deathday + "', 'yyyy-mm-dd'), '" + known_for_department + "')"
        else:
            sql += deathday + ", '" + known_for_department + "')"
            deathday = None
        # Monta o JSON
        person = {
            "_id": personJson["id"],
            "name": name,
            "gender": personJson["gender"],
            "popularity": personJson["popularity"],
            "place_of_birth": place_of_birth,
            "birthday": birthday,
            "deathday": deathday,
            "known_for_department": known_for_department
        }
        # Executa a query sql no banco
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            responseString = "Pessoa: " + name + " salva com sucesso!"
            self.mainController.outputResponse(responseString)
        except:
            self.connection.rollback()
            pass
        try:
            # Faz a inserção do JSON no mongo
            self.mongo.people.insert_one(person)
        except:
            pass