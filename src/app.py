from flask import Flask
from flask_cors import CORS
import dotenv

from src.controllers.Home import HomeController
from src.controllers.Category import CategoryController
from src.controllers.Gallery import GalleryController
from src.controllers.Attribution import AttributionController

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(HomeController)
app.register_blueprint(CategoryController)
app.register_blueprint(GalleryController)
app.register_blueprint(AttributionController)

"""
1. 作者的描述，越多越好，尽量带作者的派别
2. 作品的题材，流派信息，用作分类
3. 作品的赏析
4. 画作名字的搜索，年代搜索，（尽量模糊）
5. 作品的相关推荐
6. 多语言
"""
