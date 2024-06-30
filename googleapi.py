import google.generativeai as genai
import os
import dotenv

from src.services.Database import Database

dotenv.load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

database = Database()

query = "select attribution from attributions order by attributionid asc;"

data = database.query(query)

for name in data:
    print(name[0], type(name[0]))

    response = model.generate_content(
        f"Give me a description of {name[0]}, answer only contains the description itself, no special charasters, not more than 2000 charasters."
    )
    print(response.text)

    break
