from flask import Blueprint

from src.services.Database import Database

GalleryController = Blueprint("Gallery", __name__)


@GalleryController.get("/gallery")
def gallery():

    database = Database()

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

    data = database.query(query)
    # {'objectid': ('integer', 'NO'), 'uuid': ('character varying', 'YES'), 'accessioned': ('integer', 'NO'),...}

    # remote the t1.,t2. prefix from columns
    columns_clean = [column.split(".")[1] for column in columns]

    # zip columns and each item in data to create a dictionary
    results = [dict(zip(columns_clean, item)) for item in data]

    return {"data": results}
