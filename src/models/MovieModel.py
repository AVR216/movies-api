from database.db import get_connection
from .entities.Movie import Movie

class MovieModel():

    @classmethod
    def get_movies(cls):
        try:
            connection = get_connection()
            movies = []
            with connection.cursor() as cursor:
                
                cursor.execute("""
                                SELECT id, title, duration, released
                                FROM movies
                                ORDER BY title, duration ASC
                               """)
                
                resulttset = cursor.fetchall()
                
                for row in resulttset:
                    movie = Movie(row[0], row[1], row[2], row[3])
                    movies.append(movie.to_JSON())
            
            connection.close()

            return movies;
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def find_movie(cls, movie_id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                
                cursor.execute("""
                                SELECT id, title, duration, released
                                FROM movies
                                WHERE id = %s 
                               """, (movie_id, ))
                
                row = cursor.fetchone()

                movie = None

                if row != None:
                    movie = Movie(row[0], row[1], row[2], row[3])
                    movie = movie.to_JSON()
                
            
            connection.close()

            return movie;
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def add_movie(cls, movie):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                
                cursor.execute("""
                                INSERT INTO movies(title, duration, released)
                                VALUES(%s, %s, %s)
                               """, (movie.title, movie.duration, movie.released))
                
                affected_rows = cursor.rowcount
                connection.commit()
                
            
            connection.close()

            return affected_rows;
        except Exception as ex:
            connection.rollback()
            raise Exception(ex)
        

    @classmethod
    def delete(cls, movie_id):
        try:
            connection = get_connection()

            

            with connection.cursor() as cursor:
                
                cursor.execute("""
                                DELETE FROM movies
                                WHERE id = %s
                               """, (movie_id, ))
                
                affected_rows = cursor.rowcount
                print(affected_rows)
                connection.commit()
                
            
            connection.close()

            return affected_rows;
        except Exception as ex:
            connection.rollback()
            raise Exception(ex)
        
    
    @classmethod
    def update(cls, movie_id, movie):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""
                                    UPDATE movies 
                                    SET title = %s, 
                                        duration = %s, 
                                        released = %s
                                    WHERE id = %s
                                    """, (movie.title, movie.duration, movie.released, movie_id))
                
                rows_affected = cursor.rowcount
                connection.commit()
            
            connection.close()
            return rows_affected
                
        except Exception as ex:
            connection.rollback()
            raise Exception(ex)