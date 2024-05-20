from flask import Flask
from flask_cors import CORS
import dotenv

from services.Database import Database
from controllers.Home import HomeController
from controllers.Gallery import GalleryController

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(HomeController)
app.register_blueprint(GalleryController)


if __name__ == "__main__":

    """
    [program:artworks]
    command = /root/artworks-server/venv/bin/python3 /root/artworks-server/venv/bin/gunicorn --chdir /root/artworks-server/ --config /root/artworks-server/gunicorn.conf app:app
    user = root  # Replace with your username
    autostart = false
    autorestart = true
    """

    app.run(host="0.0.0.0", port=6301, debug=True)
