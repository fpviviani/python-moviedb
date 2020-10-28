CREATE TABLE genres (
	id INTEGER PRIMARY KEY,
	name VARCHAR(50)
);

CREATE TABLE collections (
	id BIGINT PRIMARY KEY,
	name VARCHAR(150)
);

CREATE TABLE production_companies (
	id BIGINT PRIMARY KEY,
	name VARCHAR(150),
	origin_country VARCHAR(5)
);

CREATE TABLE production_countries (
	iso_3166_1 VARCHAR(5) PRIMARY KEY,
	name VARCHAR(50)
);

CREATE TABLE people (
	id BIGINT PRIMARY KEY,
	name VARCHAR(150),
	gender INTEGER,
	popularity FLOAT,
	place_of_birth VARCHAR(150),
	birthday DATE,
	deathday DATE, 
	know_for_department VARCHAR(50)
);


CREATE TABLE movies (
	id BIGINT PRIMARY KEY,
	original_language VARCHAR(30),
	original_title VARCHAR(150),
	popularity FLOAT,
	status VARCHAR(30),
	title VARCHAR(150),
	vote_average FLOAT,
	vote_count BIGINT,
	release_date DATE,
	budget FLOAT,
	revenue FLOAT,
	runtime INTEGER, 
	id_collection BIGINT,
		FOREIGN KEY (id_collection) REFERENCES collections(id)
);

CREATE TABLE trending_movies (
	trend_id INTEGER PRIMARY KEY,
	trend_date DATE,
	id_movie BIGINT UNIQUE, 
		FOREIGN KEY (id_movie) REFERENCES movies(id)
);

CREATE TABLE movie_production_companies (
	id_movie BIGINT, 
	id_production_company BIGINT,
	PRIMARY KEY(id_movie, id_production_company),
		FOREIGN KEY(id_movie) REFERENCES movies(id),
		FOREIGN KEY(id_production_company) REFERENCES production_companies(id)
);

CREATE TABLE movie_production_countries (
	id_movie BIGINT,
	iso_3166_1 VARCHAR(5) NOT NULL,
	PRIMARY KEY (id_movie, iso_3166_1),
		FOREIGN KEY (id_movie) REFERENCES movies(id),
		FOREIGN KEY (iso_3166_1) REFERENCES production_countries(iso_3166_1)	
);

CREATE TABLE movie_genres (
	id_movie BIGINT, 
	id_genre INTEGER NOT NULL,
	PRIMARY KEY(id_movie, id_genre),
		FOREIGN KEY (id_movie) REFERENCES movies(id),
		FOREIGN KEY (id_genre) REFERENCES genres(id)
); 

CREATE TABLE credits (
	credit_id VARCHAR(30) PRIMARY KEY,
	credit_type VARCHAR(30),
	department VARCHAR(30),
	job VARCHAR(50),
	character VARCHAR(150),
	id_movie BIGINT, 
	id_people BIGINT,
		FOREIGN KEY(id_movie) REFERENCES movies(id),
		FOREIGN KEY(id_people) REFERENCES people(id)
);

CREATE TABLE trending_people (
	trend_id INTEGER PRIMARY KEY,
	trend_date DATE,
	id_people BIGINT UNIQUE,
		FOREIGN KEY (id_people) REFERENCES people(id)
);