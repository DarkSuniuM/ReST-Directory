from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from directory.config import Development

app = Flask(__name__)
app.config.from_object(Development)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt_manager = JWTManager(app)

@app.route('/')
def home():
    return {'message': 'Hello World'}


from directory.apps.users_app import users

app.register_blueprint(users)
