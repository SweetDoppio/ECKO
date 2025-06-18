import os

basedir = os.path.abspath(os.path.dirname(__file__)) 


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ILoveBricks'
    #First term looks for value of environ variable, second variable is used as default if
    # environ does not define the variable.

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #Takes location of apps database from the config variable, and provide fallback value
    #when the environment does not define the variable.



