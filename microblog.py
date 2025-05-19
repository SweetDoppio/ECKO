from app import app
import sqlalchemy.orm as so
from sqlalchemy import __version__ as sa_version
import sqlalchemy as sa
from app import app, db
from app.models import User, Post

@app.shell_context_processor
#above decorator registers as shell context function
#When flask shell command runs, it invokes 
def make_shell_context():

    return {'sa':sa, 'so': so, 'db': db, 'User':User, 'Post':Post, 'sa_version':sa_version}


