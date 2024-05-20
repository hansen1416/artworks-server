import os
import psycopg2


class Database:

    def __init__(self) -> None:

        user = os.getenv("DB_USERNAME")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")
        # for creating connection string
        self.conn = psycopg2.connect(
            dbname=database, user=user, password=password, host=host, port=port
        )

        self.cur = self.conn.cursor()

        print("Database connection created")

    # when destructor is called
    def __del__(self):

        self.cur.close()
        self.conn.close()

        print("Database connection destroyed")

    def query(self, query):

        self.cur.execute(query)

        return self.cur.fetchall()
