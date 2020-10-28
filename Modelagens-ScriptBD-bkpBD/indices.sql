EXPLAIN ANALYSE SELECT * FROM movies;
select * from pg_indexes where tablename = 'movies';

EXPLAIN ANALYSE SELECT * FROM collections;
select * from pg_indexes where tablename = 'collections';

EXPLAIN ANALYSE SELECT * FROM credits;
select * from pg_indexes where tablename = 'credits';

EXPLAIN ANALYSE SELECT * FROM genres;
select * from pg_indexes where tablename = 'genres';

EXPLAIN ANALYSE SELECT * FROM movie_genres;
select * from pg_indexes where tablename = 'movie_genres';

EXPLAIN ANALYSE SELECT * FROM movie_production_companies;
select * from pg_indexes where tablename = 'movie_production_companies';

EXPLAIN ANALYSE SELECT * FROM people;
select * from pg_indexes where tablename = 'people';

EXPLAIN ANALYSE SELECT * FROM production_companies;
select * from pg_indexes where tablename = 'production_companies';

EXPLAIN ANALYSE SELECT * FROM trending_movies;
select * from pg_indexes where tablename = 'trending_movies';

EXPLAIN ANALYSE SELECT * FROM trending_people;
select * from pg_indexes where tablename = 'trending_people';