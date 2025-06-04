from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, regexp, InputRequired,ValidationError, Email, EqualTo
from app.models import User
from app import db
import sqlalchemy as sa

validators=Length(min=8,max=30)

class LoginForm(FlaskForm):
    username = StringField('Full Name', validators=[DataRequired('No username input detected')])
    email = EmailField('Email',  validators=[DataRequired('No email detected'), regexp(r'^[\w\.-]+@[\w\.-]+\.\w+$',message='Entered mail is not a valid format')])
    password = PasswordField('Password', validators=[DataRequired('No password Detected')])
    submit = SubmitField('Sign in')
    accept_form = BooleanField('I accept the site rules', validators=[InputRequired('You must accept the site rules')])
    remember_me = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('Usernane', validators=[DataRequired('Please enter a valid username')])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Enter user Password', validators=[DataRequired()])
    password_confirm =PasswordField('Repeat Password', validators=[DataRequired(), EqualTo(password)])
    sumbit = SubmitField('Registetr')

    def user_validation(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please select a different name')
        
    def email_validation(self, email):
        user_email = db.session.scalar(sa.select(User).where(email == email.data))
        if user_email is not None:
            raise ValidationError('Please provide a different email')


