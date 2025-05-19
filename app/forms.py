from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, regexp, InputRequired,ValidationError, Email, EqualTo

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
        None

