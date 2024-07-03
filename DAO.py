from database.DB_connect import DBConnect
from model.movie import Movie


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getMovies():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""select *
                    from movies
                    where rank is not null""")
        cursor.execute(query, )

        for row in cursor:
            result.append(Movie(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(m1, m2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""select count(distinct r1.actor_id) as peso, r1.movie_id as movie1, r2.movie_id as movie2
                    from roles r1, roles r2
                    where r1.actor_id = r2.actor_id and r1.movie_id = %s 
                    and r2.movie_id = %s
                    group by movie1, movie2""")
        cursor.execute(query, (m1, m2))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result
