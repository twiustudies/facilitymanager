from flask import Flask
from flask_babel import Babel
from translations import babel, get_locale

def create_app():
    app = Flask(__name__)
    babel.init_app(app)
    app.config["BABEL_DEFAULT_LOCALE"] = "en"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"
    
    return app
