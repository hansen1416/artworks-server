from flask import Flask
from flask_cors import CORS
import dotenv

from src.controllers.Home import HomeController
from src.controllers.Category import CategoryController
from src.controllers.Gallery import GalleryController

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(HomeController)
app.register_blueprint(CategoryController)
app.register_blueprint(GalleryController)
