from flask import Blueprint

from src.services.Database import Database

AttributionController = Blueprint("Attribution", __name__)


@AttributionController.get("/attributions")
def Attributions():
    """
    Get a list of artisits

    :return:
        All the data is wrapped in a `data` key.
        the value in `data` is a dictionary.

        dictionary contains the following key-value pairs:
            - artworks_count: the number of artworks by the artist.
            - attribution: the name of the artist.
            - attributionid: the id of the artist.
            - beginYear: the start year of the artist.
            - classification: The category or type of artwork.
            - depictstmsobjectid: The object ID of the artwork in published_images table.
            - dimensions: The size or measurements of the artwork.
            - displayDate: The date or period of the artwork displayed.
            - endYear: The end year of the artwork.
            - iiifThumbURL: The IIIF thumbnail URL of the artwork, erplace the `width,height` in the url to get diesired size.
            - iiifURL: The IIIF URL of the artwork.
            - inscription: Any inscriptions or text on the artwork.
            - medium: The materials used to create the artwork.
            - objectID: The object ID of the artwork in objects table.
            - sequence: The sequence number of the artwork.
            - title: The title or name of the artwork.
            - uuid: The unique identifier of the artwork.
            - viewtype: The view type of the artwork.
            - width: The width of the artwork.
            - height: The height of the artwork.
    """

    database = Database()

    columns = ["attributionid", "attribution", "description", "artworks_count"]

    query = (
        f"select "
        + ",".join(columns)
        + " from attributions t1 "
        + " where t1.description is not null and t1.description != '' "
        + " order by artworks_count desc limit 10"
    )

    data = database.query(query)
    # {'objectid': ('integer', 'NO'), 'uuid': ('character varying', 'YES'), 'accessioned': ('integer', 'NO'),...}

    if not data or len(data) == 0:
        return {"data": {}}

    results = []

    subcolumns = [
        "t1.depictstmsobjectid",
        "t1.iiifURL",
        "t1.iiifThumbURL",
        "t1.viewtype",
        "t1.sequence",
        "t1.width",
        "t1.height",
        "t2.objectID",
        "t2.uuid",
        "t2.title",
        "t2.displayDate",
        "t2.beginYear",
        "t2.endYear",
        "t2.medium",
        "t2.dimensions",
        "t2.inscription",
        "t2.attribution",
        "t2.classification",
    ]

    # remote the t1.,t2. prefix from columns
    subcolumns_clean = [column.split(".")[1] for column in subcolumns]

    for row in data:
        res = dict(zip(columns, row))

        subquery = (
            f"SELECT {','.join(subcolumns)}"
            + f" FROM published_images as t1 "
            + f" left join objects as t2 on t1.depictstmsobjectid = t2.objectID"
            + f" where t2.attribution = '{res['attribution']}'"
            + "limit 1"
        )

        subdata = database.query(subquery)

        if subdata and len(subdata) > 0:
            subres = dict(zip(subcolumns_clean, subdata[0]))

        res.update(subres)

        results.append(res)

    return {"data": results}
