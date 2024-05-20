from flask import Blueprint

from services.Database import Database

HomeController = Blueprint("Home", __name__)


@HomeController.get("/home")
def home():
    """
    Ancient Art:

    This period is vast and can vary depending on the specific civilization. A common range used for Western art history is 3500 BC to 476 AD.

    Medieval Art:

    This period follows the fall of the Western Roman Empire. A general range is 476 AD to 1400 AD.

    Renaissance Art:

    Marking a rebirth of classical ideals, the Renaissance is roughly 1400 AD to 1600 AD.

    Baroque Art:

    The Baroque period is known for its drama, emotion, and movement. It falls within 1600 AD to 1750 AD.

    Modern Art:

    Modern art encompasses a wide range of styles that broke away from traditional forms. A common range is 1860s to 1970s.

    Contemporary Art:

    Contemporary art refers to art created in the recent past and present. It's generally considered to be from the 1970s to present day.
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
