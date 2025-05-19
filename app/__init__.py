from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#db object represents the database
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view='login'
#migrate represents the migration engine
from app import routes, models

if __name__ == "__main__":
    app.run(debug=True)

    ##Also need to enter 'flask run --debug --reload' to see changes.