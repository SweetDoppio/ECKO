# ECKO WVD
 REMINDER: CHECK WITH OTHERS WHEN DEALING WITH MERGE CONFLICTS



 >>> from app import app, db
>>> from app.models import User, Post
>>> import sqlalchemy as sa
For Flask and its extensions to have access to the Flask application without having to pass app as an argument into every function, an application context must be created and pushed. following code in your Python shell session:

>>> app.app_context().push()

