from flask import Blueprint

from src.services.Database import Database

GalleryController = Blueprint("Gallery", __name__)


@GalleryController.get("/object/<object_id>")
def object_by_id(object_id):
    """
    Get a single object by its ID

    :param object_id: The ID of the object

    :return:
        All the data is wrapped in a `data` key.
        the value in `data` is a dictionary.

        dictionary contains the following key-value pairs:
            - attribution: The authorship or origin of the artwork.
            - beginYear: The start year of the artwork.
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

    columns = [
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

    query = (
        f"SELECT {','.join(columns)}"
        + f" FROM published_images as t1 "
        + f" left join objects as t2 on t1.depictstmsobjectid = t2.objectID"
        + f" where t2.objectID = {object_id}"
    )

    data = database.query(query)
    # {'objectid': ('integer', 'NO'), 'uuid': ('character varying', 'YES'), 'accessioned': ('integer', 'NO'),...}

    if not data or len(data) == 0:
        return {"data": {}}

    # remote the t1.,t2. prefix from columns
    columns_clean = [column.split(".")[1] for column in columns]

    # zip columns and each item in data to create a dictionary
    results = dict(zip(columns_clean, data[0]))

    return {"data": results}
