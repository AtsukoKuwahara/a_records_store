from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restx import Api

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database object db
db = MongoEngine()
db.init_app(app)

# Initialize the API with a prefix
api = Api(app, doc='/api/doc/', prefix='/api')

# Import the routes after the app and api have been initialized
from application import routes
