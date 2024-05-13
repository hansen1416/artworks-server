import csv
import os

import dotenv
import psycopg2

dotenv.load_dotenv()


def clean_row(row, column_names, column_attributes):
    for i, data in enumerate(row):

        col_name = column_names[i]
        col_attr = column_attributes[col_name]

        # when insert empty string to an integer column, convert it to None or 0
        if data == "" and col_attr[0] == "integer":

            if col_attr[1] == "YES":
                row[i] = None
            else:
                row[i] = 0

        if data == "" and col_attr[0] == "timestamp with time zone":
            row[i] = None

    return row


def insert_rows(cursor, conn, table_name, column_names_str, rows):

    records_list_template = ",".join(["%s"] * len(rows))

    insert_query = (
        f"INSERT INTO {table_name} ({column_names_str}) VALUES {records_list_template}"
    )

    # print(insert_query)
    # print(tuple(rows))

    cursor.execute(insert_query, rows)

    conn.commit()


def load_csv(file_path, conn):

    # get the file name from the file path
    file_name = os.path.basename(file_path)
    table_name = file_name.split(".")[0]
    table_schema = "public"

    # Create a cursor object
    cur = conn.cursor()

    # get the column attributes from the database
    cur.execute(
        f"SELECT column_name, data_type, is_nullable FROM information_schema.columns"
        + f" WHERE table_schema = '{table_schema}' AND table_name = '{table_name}';"
    )

    column_attributes_list = cur.fetchall()
    # {'objectid': ('integer', 'NO'), 'uuid': ('character varying', 'YES'), 'accessioned': ('integer', 'NO'),...}
    column_attributes = {}

    for column in column_attributes_list:
        column_attributes[column[0]] = column[1:]

    conn.commit()

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")

        # iterate over the rows in the file

        column_names = next(reader)
        column_names_str = ", ".join(column_names)

        count = 1

        try:

            rows_data = []

            row = next(reader)

            while row:

                row = clean_row(row, column_names, column_attributes)

                rows_data.append(tuple(row))

                if len(rows_data) == 1000:

                    insert_rows(cur, conn, table_name, column_names_str, rows_data)

                    print(
                        f"Inserted {count-len(rows_data)} - {count} rows into {table_name}"
                    )

                    rows_data = []

                count += 1

                row = next(reader)

        except StopIteration:

            if len(rows_data) > 0:

                insert_rows(cur, conn, table_name, column_names_str, rows_data)

                print(
                    f"Inserted {count-len(rows_data)} - {count} rows into {table_name}"
                )

            print("End of file reached")

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

    csv_data_path = os.path.join(
        os.path.expanduser("~"), "NationalGalleryOfArt-opendata", "data"
    )

    files_arr = os.listdir(csv_data_path)

    # move "objects.csv" to the start of the list
    files_arr.remove("objects.csv")
    files_arr.insert(0, "objects.csv")

    # search the position of `media_items.csv` in the list
    media_items_index = files_arr.index("objects_historical_data.csv")
    # keep only the files after `media_items.csv`
    files_arr = files_arr[media_items_index:]

    # list all the files in the directory
    for file in files_arr:

        file_path = os.path.join(csv_data_path, file)

        # file_path = "objects.csv"
        # file_path = "published_images.csv"

        conn = postgres_connection()

        load_csv(file_path, conn)

    pass
