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
        + f" where t2.description is not null and t2.description != '' "
        + f" and classification in ('Drawing', 'Sculpture', 'Photograph', 'Painting') "
        + f" and title is not null and title != ''"
        + f" order by t2.objectid asc;"
    )

    data = database.query(query)

    for row in data:

        response = model.generate_content(
            f"Give me a description of {row[1]}, which is an artwork by {row[2]} answer only contains the description itself, no special charasters, not more than 3000 charasters."
        )
        # print(response.text)

        try:

            # break
            # escape the single quotes in the response text
            description = response.text.replace("'", "''")

            print(description)
            print("=====================================")

            # # save the response to the database, column `description` of table `objects`
            # query = f"update objects set description = E'{description}' where object = '{row[0]}';"

            # print(
            #     f"description saved for {row[0]}, {row[1]}, description length {len(description)}."
            # )

            # database.execute(query)

        except Exception as e:
            print(f"Error: {e}")

        # Pause execution for 2 seconds
        time.sleep(3)


if __name__ == "__main__":

    generate_objects_description()
