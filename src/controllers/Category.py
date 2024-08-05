from flask import Blueprint, request

from src.services.Database import Database
from src.constants import YEARS_RANGE, SUBJECT_MATTER_CATEGORIES

CategoryController = Blueprint("Category", __name__)


@CategoryController.get("/categories")
def categories():
    """
    Categories endpoint.

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
                    "category_type":"year",
                    "category_id":1,
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
                    ]
                },
                ...
            ]
            ...
        }

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

    results = []

    for year_range in YEARS_RANGE:
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
                "category_type": "year",
                "category_id": year_range[3],
                "year_range": [year_range[1], year_range[2]],
                "data": [dict(zip(columns_clean, item)) for item in data],
            }
        )

    return {"data": results}


@CategoryController.get("/category/year/<int:id>")
def category_year(id):
    """
    Category Year endpoint.

    Get 50 random artworks from a specific year range.

    :param id: The year range ID.
    :param page: url get parameter, `page` index of data
    :param page_size: url get parameter, `page_size` index of data

    :return:
        All the data is wrapped in a `data` key.
        the value in `data` is a list of dictionaries, where each dictionary represents an artwork.

        Each dictionary contains the following key-value pairs:
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

    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)

    year_range_info = None

    for info in YEARS_RANGE:
        if info[3] == id:
            year_range_info = info
            break

    if year_range_info is None:
        return {"error": "Invalid year range ID"}

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
        + f" where t2.endYear is not null and t2.endYear != 0 "
        + f" and t2.endYear >= {year_range_info[1]} and t2.endYear < {year_range_info[2]} "
        + f" order by t2.objectID asc "
        + f" limit {page_size} offset {(page - 1) * page_size}"
    )

    data = database.query(query)

    # remote the t1.,t2. prefix from columns
    columns_clean = [column.split(".")[1] for column in columns]

    return {"data": [dict(zip(columns_clean, item)) for item in data]}


@CategoryController.get("/categories/subjects")
def categories_subjects():
    """
    Categories endpoint.

    :return:
        All the data is wrapped in a `data` key.
        the value in `data` is a list of dictionaries, where each dictionary represents an artwork category.

        Each dictionary contains a `category` which is the name of the art category,
        there are 3 categories in total: 1. landscape, 2. portrait, and 3. still life
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
            - subject_matter_category_id: 1. landscape, 2. portrait, 3. still life

    Example::

        {
            "data": [
                {
                    "category": "Landscape",
                    "category_id": 1,
                    "category_type": "subject_matter",
                    "data": [
                        {
                            "attribution": "Robert Austin",
                            "beginYear": 1922,
                            "classification": "Drawing",
                            "depictstmsobjectid": 4222,
                            "dimensions": "overall: 13.9 x 9.2 cm (5 1/2 x 3 5/8 in.)",
                            "displayDate": "1922",
                            "endYear": 1922,
                            "height": 4225,
                            "iiifThumbURL": "https://api.nga.gov/iiif/7f9cb267-13ac-48ff-9b9c-e9ddf4e10f80/full/!200,200/0/default.jpg",
                            "iiifURL": "https://api.nga.gov/iiif/7f9cb267-13ac-48ff-9b9c-e9ddf4e10f80",
                            "inscription": "lower right in graphite: Austin / Sept / 22; 14; lower left in graphite, circled: 1",
                            "medium": "graphite on wove paper",
                            "objectID": 4222,
                            "sequence": "0",
                            "subject_matter_category_id": 1,
                            "title": "Study for \"The Angelus\"",
                            "uuid": null,
                            "viewtype": "primary",
                            "width": 2774
                        },
                    ...
                    ]
                },
                ...
            ]
            ...
        }
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
        "t2.subject_matter_category_id",
    ]

    results = []

    for subject_matter in SUBJECT_MATTER_CATEGORIES:

        subject_matter_name, subject_matter_id = subject_matter

        # select 10 items from each year range randomly
        query = (
            f"SELECT {','.join(columns)}"
            + f" FROM published_images as t1 "
            + f" left join objects as t2 on t1.depictstmsobjectid = t2.objectID"
            + f" where t2.subject_matter_category_id = {subject_matter_id} "
            + f" and t2.description is not null and t2.description != '' "
            + f" order by random() "
            + f" limit 10;"
        )

        data = database.query(query)

        # remote the t1.,t2. prefix from columns
        columns_clean = [column.split(".")[1] for column in columns]

        # zip columns and each item in data to create a dictionary
        results.append(
            {
                "category": subject_matter_name,
                "category_type": "subject_matter",
                "category_id": subject_matter_id,
                "year_range": [None, None],
                "data": [dict(zip(columns_clean, item)) for item in data],
            }
        )

    return {"data": results}


@CategoryController.get("/category/subject/<int:id>")
def category_subject(id):
    """
    Category Year endpoint.

    Get 50 random artworks from a specific year range.

    :param id: The subject_matter_category_id. 1. landscape, 2. portrait, 3. still life
    :param page: url get parameter, `page` index of data
    :param page_size: url get parameter, `page_size` index of data

    :return:
        All the data is wrapped in a `data` key.
        the value in `data` is a list of dictionaries, where each dictionary represents an artwork.

        Each dictionary contains the following key-value pairs:
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
            - subject_matter_category_id: 1. landscape, 2. portrait, 3. still life
    """

    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)

    subject_matter_info = None

    for info in SUBJECT_MATTER_CATEGORIES:
        if info[1] == id:
            subject_matter_info = info
            break

    if subject_matter_info is None:
        return {"error": "Invalid subject matter category id"}

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
        "t2.subject_matter_category_id",
    ]

    query = (
        f"SELECT {','.join(columns)}"
        + f" FROM published_images as t1 "
        + f" left join objects as t2 on t1.depictstmsobjectid = t2.objectID"
        + f" where t2.subject_matter_category_id = {id} "
        + f" and t2.description is not null and t2.description != '' "
        + f" order by t2.objectID asc "
        + f" limit {page_size} offset {(page - 1) * page_size}"
    )

    data = database.query(query)

    # remote the t1.,t2. prefix from columns
    columns_clean = [column.split(".")[1] for column in columns]

    return {"data": [dict(zip(columns_clean, item)) for item in data]}
