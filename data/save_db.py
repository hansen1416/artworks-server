import csv
import os

import dotenv
import psycopg2

dotenv.load_dotenv()


def load_csv(file_path, conn):

    # get the file name from the file path
    file_name = os.path.basename(file_path)
    tanble_name = file_name.split(".")[0]

    # Create a cursor object
    cur = conn.cursor()

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")

        # iterate over the rows in the file

        # headers = []
        column_names = None

        for i, row in enumerate(reader):
            if i == 0:
                # Get column names and values from the dictionary
                column_names = ", ".join(row)
                continue

            values = tuple(row)  # Convert dictionary values to a tuple for placeholder

            # Construct the INSERT statement with placeholder for values
            insert_query = f"INSERT INTO {tanble_name} ({column_names}) VALUES %s"

            # print(insert_query)

            # todo check the column type, if its integer, convert the value to integer

            # Execute the query with the values tuple
            cur.execute(insert_query, (values,))

            # Commit the changes to the database
            conn.commit()

        # Close the connection
        cur.close()
        conn.close()


def postgres_connection():
    # for postgreSQL database credentials can be written as
    user = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    # for creating connection string
    conn = psycopg2.connect(
        dbname=database, user=user, password=password, host=host, port=port
    )

    return conn


if __name__ == "__main__":

    # for postgreSQL database credentials can be written as

    file_path = "objects.csv"

    conn = postgres_connection()

    load_csv(file_path, conn)

    pass
