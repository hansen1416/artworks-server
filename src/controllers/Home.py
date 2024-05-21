from flask import Blueprint

from src.services.Database import Database

HomeController = Blueprint("Home", __name__)


@HomeController.get("/home")
def home():
    """
    Home page endpoint.

    :return:
        All the data is wrapped in a `data` key.
        the value in `data` is a list of dictionaries, where each dictionary represents an artwork category.

        Each dictionary contains a `category` which is the name of the art category,
        there are 6 categories in total: Ancient (3500 BC to 476 AD), Medieval (476 AD to 1400 AD),
        Renaissance (1400 AD to 1600 AD), Baroque (1600 AD to 1750 AD), Modern (1860s to 1970s),
        and Contemporary (1970s to present day).
        and a `data` key which contains a list of artworks in that category. The list of items is selected randomly from the database.

        The nested `data` contains the following key-value pairs:
            - attribution: The authorship or origin of the artwork.
            - beginYear: The start year of the artwork.
            - classification: The category or type of artwork.
            - depictstmsobjectid: The object ID of the artwork in published_images table.
            - dimensions: The size or measurements of the artwork.
            - displayDate: The date or period of the artwork displayed.
            - endYear: The end year of the artwork.
            - height: The height of the artwork.
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

    Example::

        {
            "data": [
                {
                    "category":"Ancient",
                    "data":[
                        {
                            "attribution":"Boeotian 3rd Century B.C.",
                            "beginYear":-300,"classification":"Sculpture",
                            "depictstmsobjectid":177238,
                            "dimensions":"height: 22.9 cm (9 in.)","displayDate":"3rd century B.C.",
                            "endYear":-200,
                            "height":9790,
                            "iiifThumbURL":"https://api.nga.gov/iiif/221217c8-dac5-45b6-948c-743bac837799/full/!200,200/0/default.jpg",
                            "iiifURL":"https://api.nga.gov/iiif/221217c8-dac5-45b6-948c-743bac837799",
                            "inscription":"",
                            "medium":"terracotta",
                            "objectID":177238,
                            "sequence":"1",
                            "title":"Standing Woman with Fan",
                            "uuid":null,
                            "viewtype":"alternate",
                            "width":6993
                        },
                        ...
                    ]}
                },
                ...
            ]
            ...
        }

    """

    years_range = [
        ("Ancient", -3500, 476),
        ("Medieval", 476, 1400),
        ("Renaissance", 1400, 1600),
        ("Baroque", 1600, 1750),
        ("Modern", 1860, 1970),
        ("Contemporary", 1970, 3000),
    ]

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

    results = []

    for year_range in years_range:
        # select 10 items from each year range randomly
        query = (
            f"SELECT {','.join(columns)}"
            + f" FROM published_images as t1 "
            + f" left join objects as t2 on t1.depictstmsobjectid = t2.objectID"
            + f" where t2.endYear is not null and t2.endYear != 0 "
            + f" and t2.endYear >= {year_range[1]} and t2.endYear < {year_range[2]} "
            + f" order by random() "
            + f" limit 10;"
        )

        data = database.query(query)

        # remote the t1.,t2. prefix from columns
        columns_clean = [column.split(".")[1] for column in columns]

        # zip columns and each item in data to create a dictionary
        results.append(
            {
                "category": year_range[0],
                "year_range": [year_range[1], year_range[2]],
                "data": [dict(zip(columns_clean, item)) for item in data],
            }
        )

    return {"data": results}
