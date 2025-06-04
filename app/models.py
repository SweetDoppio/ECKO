from typing import Optional
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone
import sqlalchemy as sa
#includes general purpose db functions and classes
import sqlalchemy.orm as so
#provides support using models
from app import db
from flask_login import UserMixin
from app import login

@login.user_loader
#user loader is registered with flask_login with this decorator
#id gets passed to this function as a argument, so needs to be convereted to int first
def user_loader(id):
    return db.session.get(User, int(id))

class User(UserMixin,db.Model):
    #class User will inherit from the db Model(base class for all FLASK-SQLalchemy)
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    #Declariing a class attribute that will be a database column.
    # mapped_column method 
    #Type hint/annotations indicates the expected data types of variables.
    username: so.Mapped[str] = so.mapped_column(sa.String(20),index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(30), index=True, unique=True) 
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50))
    #Optional allows this column to be empty or nullable.
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    #'posts' is the many side, the WOM class is for large relationships  where you dont need to
    #load the full list of items. 'Post' refers to the object.
    #And defines 'posts' as a collection type with Post obj inside.
    #first argument to the the relationship function is the model class that represents other
    #side of the relationship

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        #repr method tells python how to print object of this class
        return '<User {}, Email>'.format(self.username, self.email)

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(200))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True,default=lambda: datetime.now(timezone.utc))
    #when passing a function as a default, SQLAlcehmy sets the field to the value returned by the function
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    #user_id field is initialised as a foreignKey to User.id: References value from the id column in Users table
    author: so.Mapped[User] = so.relationship(back_populates='posts')
    #back_populates argument references the name of the rel attribute on the other side.
    #Referening the class 'User' above. 



#terminal command to add user manually --From python terminal:
#   python
# >>> from app import app, db
# >>> from app.models import User, Post
# >>> import sqlalchemy as sa

#>>> app.app_context().push()
# u = User(username='Mary',email='example@mail.com')
# db.session.add(u)
# db.session.commit()

#Terminal command to return the iterator to check user database
# >>> users=db.session.scalars(query).all()
# >>> for user in users:
# ...     print(user.id, user.useename, user.email)
