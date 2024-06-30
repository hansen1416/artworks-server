import google.generativeai as genai
import os
import dotenv

from src.services.Database import Database

dotenv.load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

database = Database()

query = "select attribution, attribution from attributions order by attributionid asc;"

data = database.query(query)

for name in data:
    print(name[1], type(name[1]))

    response = model.generate_content(
        f"Give me a description of {name[1]}, answer only contains the description itself, no special charasters, not more than 2000 charasters."
    )
    print(response.text)

    break

    # save the response to the database, column `description` of table `attributions`
    query = f"update attributions set description = '{response.text}' where attribution = '{name[0]}';"
