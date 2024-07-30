import google.generativeai as genai
import os
import dotenv
import time

from src.services.Database import Database

dotenv.load_dotenv()


def get_model():

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    return genai.GenerativeModel("gemini-1.5-flash")


def generate_attributions_description():

    model = get_model()

    database = Database()

    query = "select attributionid, attribution from attributions where description is null or description = '' order by attributionid asc;"

    data = database.query(query)

    for name in data:

        response = model.generate_content(
            f"Give me a description of {name[1]}, answer only contains the description itself, no special charasters, not more than 2000 charasters."
        )
        # print(response.text)

        try:

            # break
            # escape the single quotes in the response text
            description = response.text.replace("'", "''")

            # save the response to the database, column `description` of table `attributions`
            query = f"update attributions set description = E'{description}' where attribution = '{name[0]}';"

            print(
                f"description saved for {name[0]}, {name[1]}, description length {len(description)}."
            )

            database.execute(query)

        except Exception as e:
            print(f"Error: {e}")

        # Pause execution for 2 seconds
        time.sleep(3)


def generate_objects_description():

    model = get_model()

    database = Database()

    query = (
        f"SELECT t2.objectid, t2.title, t2.attribution, t2.classification"
        + f" FROM published_images as t1 "
        + f" left join objects as t2 on t1.depictstmsobjectid = t2.objectID"
        + f" where (t2.description is null or t2.description = '') "
        + f" and t2.classification in ('Drawing', 'Sculpture', 'Photograph', 'Painting') "
        + f" and t2.title is not null and t2.title != ''"
        + " group by t2.objectid"
        + f" order by t2.objectid asc;"
    )

    data = database.query(query)

    for row in data:

        response = model.generate_content(
            f"Give me an art Commentary of {row[1]}, which is an artwork by {row[2]} answer only contains the description itself, no special charasters, not more than 3000 charasters."
        )
        # print(response.text)

        try:

            # break
            # escape the single quotes in the response text
            description = response.text.replace("'", "''")

            # save the response to the database, column `description` of table `objects`
            query = f"update objects set description = E'{description}' where objectid = '{row[0]}';"

            print(
                f"description saved for {row[0]}, {row[1]}, description length {len(description)}."
            )

            database.execute(query)

        except Exception as e:

            query = (
                f"update objects set description = 'error' where objectid = '{row[0]}';"
            )

            print(f"Error: {e}")

        # Pause execution for 2 seconds
        time.sleep(5)


def subject_matter_categorization():
    """
    1 | landscape
    2 | portrait
    3 | still life
    """

    categories = ["landscape", "portrait", "still life"]

    model = get_model()

    database = Database()

    query = (
        f"SELECT t2.objectid, t2.title, t2.attribution, t2.classification"
        + f" FROM published_images as t1 "
        + f" left join objects as t2 on t1.depictstmsobjectid = t2.objectID"
        + f" where t2.description is not null an t2.description != '' "
        + f" and t2.subject_matter_category_id is null "
        # + f" and t2.classification in ('Drawing', 'Sculpture', 'Photograph', 'Painting') "
        # + f" and t2.title is not null and t2.title != ''"
        + " group by t2.objectid"
        + f" order by t2.objectid asc;"
    )

    data = database.query(query)

    for row in data:

        query = (
            f"The artwork named {row[1]}, the author is {row[2]},"
            + f" categorize it by subject matter, choose among : {','.join([f'{i+1}. {cat}' for i,cat in enumerate(categories)])}.'"
            + f" return only the index, 1, 2 or 3, nothing else."
        )

        # print(query)

        response = model.generate_content(query)
        # print(response.text)

        category_id = int(response.text)

        try:

            # break
            # escape the single quotes in the response text

            # save the response to the database, column `description` of table `objects`
            query = f"update objects set subject_matter_category_id = {category_id} where objectid = '{row[0]}';"

            print(
                f"subject_matter_category_id saved for {row[0]}, {row[1]}, category_id {category_id}."
            )

            database.execute(query)

        except Exception as e:

            query = f"update objects set subject_matter_category_id = 0 where objectid = '{row[0]}';"

            print(f"Error: {e}")

        # Pause execution for 2 seconds
        time.sleep(5)


if __name__ == "__main__":

    subject_matter_categorization()
