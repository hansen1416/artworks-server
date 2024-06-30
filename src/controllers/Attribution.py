from flask import Blueprint

from src.services.Database import Database

AttributionController = Blueprint("Attribution", __name__)


@AttributionController.get("/attributions")
def Attributions():
    """ """

    database = Database()

    columns = [
        "t1.attribution",
        "t1.description",
        "t1.artworks_count",
        # "t2.objectID",
        # "t2.uuid",
        # "t2.title",
        # "t2.displayDate",
        # "t2.beginYear",
        # "t2.endYear",
        # "t2.medium",
        # "t2.dimensions",
        # "t2.inscription",
        # "t2.attribution",
        # "t2.classification",
        # "t3.depictstmsobjectid",
        # "t3.iiifURL",
        # "t3.iiifThumbURL",
        # "t3.viewtype",
        # "t3.sequence",
        # "t3.width",
        # "t3.height",
    ]

    query = (
        f"select "
        + ",".join(columns)
        + " from attributions t1 "
        + " left join (select objectID from objects where attribution = t1.attribution limit 1) t2 on t1.attribution = t2.attribution"
        + " where t1.description is not null and t1.description != '' "
        + " order by artworks_count desc;"
    )

    data = database.query(query)
    # {'objectid': ('integer', 'NO'), 'uuid': ('character varying', 'YES'), 'accessioned': ('integer', 'NO'),...}

    if not data or len(data) == 0:
        return {"data": {}}

    # remote the t1.,t2. prefix from columns
    columns_clean = [column.split(".")[1] for column in columns]

    # zip columns and each item in data to create a dictionary
    results = [dict(zip(columns_clean, row)) for row in data]

    return {"data": results}
