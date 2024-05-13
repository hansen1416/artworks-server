import os

from flask import Flask
from flask_cors import CORS
import dotenv
import psycopg2

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)


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


@app.route("/")
def home():

    conn = postgres_connection()

    # Create a cursor object
    cur = conn.cursor()

    columns = [
        "t1.objectID",
        "t1.uuid",
        "t1.title",
        "t1.displayDate",
        "t1.beginYear",
        "t1.endYear",
        "t2.depictstmsobjectid",
        "t2.iiifURL",
        "t2.iiifThumbURL",
        "t2.viewtype",
        "t2.sequence",
        "t2.width",
        "t2.height",
    ]

    query = (
        f"SELECT {','.join(columns)}"
        + f" FROM published_images as t2 "
        + f" left join objects as t1 on t2.depictstmsobjectid = t1.objectID"
        + f" limit 10;"
    )

    # get the column attributes from the database
    cur.execute(query)

    data = cur.fetchall()
    # {'objectid': ('integer', 'NO'), 'uuid': ('character varying', 'YES'), 'accessioned': ('integer', 'NO'),...}

    cur.close()
    conn.close()

    # zip columns and each item in data to create a dictionary
    results = [dict(zip(columns, item)) for item in data]

    return {"data": results}
